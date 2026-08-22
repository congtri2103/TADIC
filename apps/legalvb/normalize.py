import re
from datetime import datetime

SO_HIEU_PATTERN = re.compile(r"\d+[A-Za-z]*/\d{4}/[A-ZĐ\-]+", re.UNICODE)


def _local(tag: str) -> str:
    return tag.split('}', 1)[-1] if '}' in tag else tag


def _child_text(elem, name):
    if elem is None:
        return None
    for child in elem.iter():
        if _local(child.tag) == name and child.text:
            return child.text.strip()
    return None


def _fix_url(url: str) -> str:
    # Feed moc.gov.vn thiếu "//" sau scheme (VD: "http:moc.gov.vn/...").
    if url.startswith('http:') and not url.startswith('http://'):
        return 'http://' + url[len('http:'):]
    if url.startswith('https:') and not url.startswith('https://'):
        return 'https://' + url[len('https:'):]
    return url


def _parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).date()
    except ValueError:
        return None


def find_so_hieu(text):
    if not text:
        return None
    m = SO_HIEU_PATTERN.search(text)
    return m.group(0) if m else None


def extract_so_hieu(title: str) -> str:
    return find_so_hieu(title) or (title or '').strip()[:100]


RSS_DATE_FORMATS = ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y')


def _parse_rss_date(value):
    if not value:
        return None
    for fmt in RSS_DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    return None


def from_vbpl_item(elem) -> dict:
    """Chuẩn hoá 1 <VanBanItem> XML từ SOAP ws.vbpl.vn về schema chung."""
    so_hieu = _child_text(elem, 'VBPQSokyhieu') or extract_so_hieu(_child_text(elem, 'Title'))
    return {
        'so_hieu':          so_hieu,
        'loai_vb':          _child_text(elem, 'VBPQLoaivanbanTitle') or '',
        'co_quan_ban_hanh': _child_text(elem, 'VBPQCoquanbanhanh') or '',
        'ngay_ban_hanh':    _parse_dt(_child_text(elem, 'VBPQNgayBanHanh')),
        'ngay_hieu_luc':    _parse_dt(_child_text(elem, 'VBPQNgaycohieuluc')),
        'trich_yeu':        _child_text(elem, 'VBPQTrichYeu') or _child_text(elem, 'Title') or '',
        'linh_vuc':         _child_text(elem, 'VBPQLinhVuc') or '',
        'trang_thai_raw':   _child_text(elem, 'VBPQTinhTrangHieuLuc') or '',
        'url_goc':          _child_text(elem, 'VBPQCTListUrl') or '',
        'url_file':         '',
        'nguon':            'vbpl_api',
    }


def from_rss_entry(entry) -> dict:
    """Chuẩn hoá 1 entry feedparser (moc.gov.vn RSS) về schema chung.

    Số hiệu văn bản thường KHÔNG nằm trong tiêu đề (tiêu đề chỉ là câu giới
    thiệu), mà nằm trong phần mô tả (VD: "...có Thông tư số 65/2026/TT-BXD
    ban hành..."), nên phải tìm trong cả title lẫn summary.
    """
    title = getattr(entry, 'title', '') or ''
    summary = getattr(entry, 'summary', '') or ''
    so_hieu = find_so_hieu(title) or find_so_hieu(summary) or extract_so_hieu(title)

    ngay_ban_hanh = None
    if getattr(entry, 'published_parsed', None):
        ngay_ban_hanh = datetime(*entry.published_parsed[:6]).date()
    else:
        ngay_ban_hanh = _parse_rss_date(getattr(entry, 'published', ''))

    return {
        'so_hieu':          so_hieu,
        'loai_vb':          '',
        'co_quan_ban_hanh': 'Bộ Xây dựng',
        'ngay_ban_hanh':    ngay_ban_hanh,
        'ngay_hieu_luc':    None,
        'trich_yeu':        title,
        'linh_vuc':         '',
        'trang_thai_raw':   '',
        'url_goc':          _fix_url(getattr(entry, 'link', '') or ''),
        'url_file':         '',
        'nguon':            'moc_rss',
    }


TRANG_THAI_MAP = {
    'còn hiệu lực':     'con_hieu_luc',
    'hết hiệu lực':     'het_hieu_luc',
    'hết hiệu lực một phần': 'sua_doi_bo_sung',
    'sửa đổi bổ sung':  'sua_doi_bo_sung',
    'chưa có hiệu lực': 'chua_co_hieu_luc',
}


def map_trang_thai(raw: str) -> str:
    return TRANG_THAI_MAP.get((raw or '').strip().lower(), 'khong_ro')
