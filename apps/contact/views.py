import json
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ContactSubmission

logger = logging.getLogger(__name__)


@require_POST
def submit(request):
    """
    POST /contact/submit/
    Body: JSON { name, email, phone, organization, product_interest, message }
    CSRF token gửi qua header X-CSRFToken.
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Dữ liệu không hợp lệ.'}, status=400)

    name  = str(data.get('name',  '')).strip()
    email = str(data.get('email', '')).strip()
    phone = str(data.get('phone', '')).strip()

    if not name:
        return JsonResponse({'error': 'Vui lòng nhập họ tên.'}, status=400)
    if not email:
        return JsonResponse({'error': 'Vui lòng nhập địa chỉ email.'}, status=400)
    if not phone:
        return JsonResponse({'error': 'Vui lòng nhập số điện thoại.'}, status=400)
    if len(name) > 100 or len(email) > 254 or len(phone) > 20:
        return JsonResponse({'error': 'Thông tin nhập vào vượt quá giới hạn cho phép.'}, status=400)

    organization     = str(data.get('organization',     '')).strip()[:200]
    product_interest = str(data.get('product_interest', 'all'))[:50]
    message          = str(data.get('message',          '')).strip()

    submission = ContactSubmission.objects.create(
        name=name, email=email, phone=phone,
        organization=organization,
        product_interest=product_interest,
        message=message,
    )

    # ── Gửi email thông báo nội bộ (nếu đã cấu hình SMTP) ──────────────────
    admin_email = getattr(settings, 'ADMIN_NOTIFY_EMAIL', '')
    if admin_email:
        try:
            subject = f'[TADIC] Yêu cầu tư vấn mới từ {name}'
            body = (
                f'Tên: {name}\nEmail: {email}\nĐiện thoại: {phone}\n'
                f'Cơ quan: {organization or "—"}\n'
                f'Sản phẩm quan tâm: {product_interest}\n'
                f'Nội dung:\n{message or "—"}\n\n'
                f'Xem admin: /admin/contact/contactsubmission/{submission.pk}/change/'
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [admin_email], fail_silently=True)
        except Exception as exc:
            logger.warning('Không gửi được email: %s', exc)

    return JsonResponse({
        'success': True,
        'message': f'Cảm ơn {name}! Yêu cầu tư vấn đã được ghi nhận. Đội ngũ kỹ sư TADIC sẽ liên hệ lại trong 24 giờ làm việc.',
    })
