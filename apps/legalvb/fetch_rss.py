import logging
import os
import ssl
import urllib.error
import urllib.request

import feedparser

from .normalize import from_rss_entry

logger = logging.getLogger(__name__)


def _ssl_context():
    # moc.gov.vn không gửi đủ chain chứng chỉ trung gian trong handshake —
    # trình duyệt/curl tự bù qua OS trust store (AIA fetching), nhưng
    # ssl module của Python thì không => bỏ qua verify riêng cho feed này.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_rss() -> list[dict]:
    """Đọc RSS Bộ Xây dựng từ MOC_RSS_URL (env). Không raise — trả [] nếu
    chưa cấu hình URL hoặc feed không đọc được (đổi cấu trúc/đổi URL)."""
    url = os.getenv('MOC_RSS_URL', '').strip()
    if not url:
        logger.info('fetch_rss: MOC_RSS_URL chưa cấu hình, bỏ qua nguồn RSS.')
        return []

    # Tự tải bytes bằng urllib (nhanh, ổn định) rồi mới đưa cho feedparser
    # parse thuần túy — để feedparser tự fetch qua http(s) rất chậm/không ổn
    # định với chain chứng chỉ thiếu của moc.gov.vn.
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (TADIC legal-doc-sync)'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
            raw = resp.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        logger.error('fetch_rss: lỗi tải feed %s: %s', url, exc)
        return []

    try:
        feed = feedparser.parse(raw)
    except Exception as exc:  # feedparser hiếm khi raise nhưng phòng hờ định dạng lỗi
        logger.error('fetch_rss: lỗi parse feed %s: %s', url, exc)
        return []

    if feed.bozo and not feed.entries:
        logger.error('fetch_rss: feed %s lỗi định dạng: %s', url, feed.get('bozo_exception'))
        return []

    return [from_rss_entry(entry) for entry in feed.entries]
