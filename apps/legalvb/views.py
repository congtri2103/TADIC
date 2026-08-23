import hmac
import io
import os

from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import render
from home.models import Product

from .models import VanBanPhapLuat


def _base_ctx():
    return {
        'nav_solutions': Product.objects.filter(is_active=True, kind='solution'),
        'nav_products':  Product.objects.filter(is_active=True, kind='product'),
    }


def van_ban_list(request):
    qs = VanBanPhapLuat.objects.filter(hien_thi=True)

    linh_vuc = request.GET.get('linh_vuc', '').strip()
    if linh_vuc:
        qs = qs.filter(linh_vuc__icontains=linh_vuc)

    trang_thai = request.GET.get('trang_thai', '').strip()
    if trang_thai:
        qs = qs.filter(trang_thai_hieu_luc=trang_thai)

    ctx = _base_ctx()
    ctx.update({
        'van_bans':   qs,
        'page_title': 'Văn bản pháp lý',
        'page_desc':  'Cập nhật Thông tư, Nghị định, QCVN, TCVN... liên quan đến đường bộ và hạ tầng giao thông do Bộ Xây dựng ban hành.',
    })
    return render(request, 'legalvb/van_ban_list.html', ctx)


def van_ban_api(request):
    qs = VanBanPhapLuat.objects.filter(hien_thi=True)

    linh_vuc = request.GET.get('linh_vuc', '').strip()
    if linh_vuc:
        qs = qs.filter(linh_vuc__icontains=linh_vuc)

    trang_thai = request.GET.get('trang_thai', '').strip()
    if trang_thai:
        qs = qs.filter(trang_thai_hieu_luc=trang_thai)

    data = [
        {
            'so_hieu': v.so_hieu,
            'loai_vb': v.loai_vb,
            'co_quan_ban_hanh': v.co_quan_ban_hanh,
            'ngay_ban_hanh': v.ngay_ban_hanh.isoformat() if v.ngay_ban_hanh else None,
            'ngay_hieu_luc': v.ngay_hieu_luc.isoformat() if v.ngay_hieu_luc else None,
            'trich_yeu': v.trich_yeu,
            'linh_vuc': v.linh_vuc,
            'trang_thai_hieu_luc': v.trang_thai_hieu_luc,
            'url_goc': v.url_goc,
            'url_file': v.url_file,
        }
        for v in qs
    ]
    return JsonResponse({'count': len(data), 'results': data})


def cron_sync(request):
    """Endpoint cho Vercel Cron gọi định kỳ (xem `crons` trong vercel.json).

    Vercel không có systemd timer như VPS, nên lịch đồng bộ được chạy bằng
    Cron Job của Vercel — nó gọi URL này kèm header `Authorization: Bearer
    $CRON_SECRET`. Bắt buộc phải có CRON_SECRET: nếu không, đây là một endpoint
    mở cho phép bất kỳ ai kích hoạt fetch mạng + ghi DB + gửi cảnh báo.
    """
    secret = os.getenv('CRON_SECRET', '').strip()
    if not secret:
        return JsonResponse(
            {'error': 'CRON_SECRET chưa được cấu hình trên môi trường này.'},
            status=503,
        )

    if not hmac.compare_digest(request.headers.get('Authorization', ''), f'Bearer {secret}'):
        return JsonResponse({'error': 'unauthorized'}, status=401)

    out = io.StringIO()
    try:
        call_command('sync_vanban', stdout=out, stderr=out)
    except Exception as exc:  # noqa: BLE001 — cron không được phép 500 vì lỗi nguồn
        return JsonResponse({'ok': False, 'error': str(exc)}, status=502)

    return JsonResponse({
        'ok': True,
        'total': VanBanPhapLuat.objects.count(),
        'output': out.getvalue().strip().splitlines(),
    })
