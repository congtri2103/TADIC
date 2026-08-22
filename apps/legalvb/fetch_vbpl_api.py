import logging
import os
import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from .normalize import from_vbpl_item

logger = logging.getLogger(__name__)

SOAP_ACTION = 'TimKiemVanBanNew'
NS = {'t': 'http://tempuri.org/'}

ENVELOPE = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <TimKiemVanBanNew xmlns="http://tempuri.org/">
      <Keyword>{keyword}</Keyword>
      <CoQuanBanHanh></CoQuanBanHanh>
      <LinhVucPhapLuat></LinhVucPhapLuat>
      <SearchDenNgay xsi:nil="true" />
      <SearchTuNgay xsi:nil="true" />
      <TrangThaiBienTap>0</TrangThaiBienTap>
      <rowPerPage>{row_per_page}</rowPerPage>
      <currentPage>1</currentPage>
      <FieldSort></FieldSort>
      <Ascending>false</Ascending>
    </TimKiemVanBanNew>
  </soap:Body>
</soap:Envelope>"""


def _ssl_context():
    # ws.vbpl.vn phục vụ chứng chỉ không khớp hostname (đã xác minh thủ công) — bỏ qua
    # verify hostname/CA cho riêng endpoint tra cứu công khai này.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_vbpl(keyword: str = '', row_per_page: int = 50) -> list[dict]:
    """Gọi SOAP action TimKiemVanBanNew trên ws.vbpl.vn, trả list dict đã chuẩn hoá.

    Lưu ý: endpoint đã xác nhận sống (200 OK) nhưng giá trị đúng của
    TrangThaiBienTap/CoQuanBanHanh chưa được xác nhận đầy đủ — có thể trả
    TotalRecord=0 cho tới khi khảo sát thêm hoặc có tài khoản CSDLQG.
    """
    base = os.getenv('VBPL_API_BASE', 'https://ws.vbpl.vn').rstrip('/')
    url = f'{base}/vbqppl.asmx'
    body = ENVELOPE.format(keyword=keyword, row_per_page=row_per_page).encode('utf-8')
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': f'http://tempuri.org/{SOAP_ACTION}',
        'User-Agent': 'Mozilla/5.0 (TADIC legal-doc-sync)',
    }
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
            raw = resp.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        logger.error('fetch_vbpl: lỗi gọi ws.vbpl.vn: %s', exc)
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        logger.error('fetch_vbpl: lỗi parse XML: %s', exc)
        return []

    items = root.findall('.//t:LtsVanBan/*', NS)
    return [from_vbpl_item(item) for item in items]
