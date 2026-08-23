import json
import logging
import os
import urllib.error
import urllib.request

logger = logging.getLogger(__name__)


def send_alert(records) -> None:
    """Gửi cảnh báo qua Zalo OA. No-op nếu chưa cấu hình ZALO_OA_ACCESS_TOKEN.

    Mặc định gọi thẳng Zalo OA API; nếu có cấu hình ZALO_OA_WEBHOOK_URL
    (VD: forward qua n8n) thì gửi tới đó thay vì gọi API trực tiếp.
    """
    token = os.getenv('ZALO_OA_ACCESS_TOKEN', '').strip()
    if not token:
        logger.info('notify_zalo: ZALO_OA_ACCESS_TOKEN chưa cấu hình, bỏ qua.')
        return
    if not records:
        return

    lines = [f"{r.so_hieu} — {r.trich_yeu}" for r in records]
    message = 'Văn bản pháp luật mới:\n' + '\n'.join(lines)

    webhook = os.getenv('ZALO_OA_WEBHOOK_URL', '').strip()
    if webhook:
        url = webhook
        payload = json.dumps({'access_token': token, 'message': message}).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
    else:
        url = 'https://openapi.zalo.me/v3.0/oa/message/cs'
        payload = json.dumps({
            'recipient': {'user_id': os.getenv('ZALO_OA_RECIPIENT_ID', '')},
            'message': {'text': message},
        }).encode('utf-8')
        headers = {'Content-Type': 'application/json', 'access_token': token}

    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        urllib.request.urlopen(req, timeout=15)
    except (urllib.error.URLError, TimeoutError) as exc:
        logger.error('notify_zalo: gửi thất bại: %s', exc)
