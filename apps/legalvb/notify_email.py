import logging
import os

from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_alert(records) -> None:
    """Gửi email cảnh báo văn bản mới khớp từ khoá ưu tiên.
    No-op nếu LEGAL_ALERT_EMAIL_TO chưa cấu hình."""
    to_addr = os.getenv('LEGAL_ALERT_EMAIL_TO', '').strip()
    if not to_addr or not records:
        return

    lines = []
    for r in records:
        lines.append(
            f"- {r.so_hieu} | {r.trich_yeu} | Ban hành: {r.ngay_ban_hanh or '?'} "
            f"| Hiệu lực: {r.ngay_hieu_luc or '?'} | {r.url_goc or ''}"
        )
    body = 'Các văn bản pháp luật mới khớp từ khoá theo dõi của TADIC:\n\n' + '\n'.join(lines)

    try:
        send_mail(
            subject=f'[TADIC] {len(records)} văn bản pháp luật mới',
            message=body,
            from_email=None,
            recipient_list=[to_addr],
            fail_silently=False,
        )
    except Exception as exc:
        logger.error('notify_email: gửi email thất bại: %s', exc)
