from django.shortcuts import render, get_object_or_404
from .models import Product, NewsArticle, Project, Testimonial, Partner, Stat

# ── Static context data ────────────────────────────────────────────────────────

ABOUT_CARDS = [
    {
        'icon': 'fa-triangle-exclamation',
        'title': 'Hạ tầng xuống cấp nhanh',
        'description': 'Hàng nghìn km đường bộ không được theo dõi định kỳ dẫn đến chi phí sửa chữa phát sinh gấp 4–10 lần bảo trì dự báo.',
    },
    {
        'icon': 'fa-person-digging',
        'title': 'Khảo sát thủ công tốn kém',
        'description': 'Phương pháp kiểm định truyền thống mất nhiều ngày, nguy hiểm và phụ thuộc hoàn toàn vào kinh nghiệm chủ quan của nhân viên.',
    },
    {
        'icon': 'fa-database',
        'title': 'Dữ liệu phân mảnh, thiếu chuẩn hóa',
        'description': 'Dữ liệu hạ tầng phân tán ở nhiều sở ngành, không liên thông và không thể khai thác để ra quyết định đầu tư dài hạn.',
    },
]

PROCESS_STEPS = [
    {
        'icon': 'fa-camera',
        'number': '01',
        'title': 'Thu thập dữ liệu thực địa',
        'description': 'Camera AI 4K lắp trên xe khảo sát thu thập hình ảnh mặt đường liên tục ở tốc độ 50–80 km/h. Cảm biến IoT và ảnh vệ tinh cung cấp dữ liệu đa chiều.',
    },
    {
        'icon': 'fa-brain',
        'number': '02',
        'title': 'Xử lý AI thời gian thực',
        'description': 'Mô hình Deep Learning phân tích và phân loại 15+ loại hư hỏng với độ chính xác >96%, gán tọa độ GPS RTK chuẩn VN-2000 cho từng điểm.',
    },
    {
        'icon': 'fa-map',
        'number': '03',
        'title': 'Số hóa & Trực quan hóa GIS',
        'description': 'Dữ liệu hư hỏng được tổng hợp thành bản đồ nhiệt GIS tương tác, bảng điều khiển theo dõi tiến độ và báo cáo PCI/IRI tự động.',
    },
    {
        'icon': 'fa-screwdriver-wrench',
        'number': '04',
        'title': 'Đề xuất & Theo dõi bảo trì',
        'description': 'Hệ thống AI tự động gợi ý phương án sửa chữa tối ưu kèm dự toán chi phí và theo dõi tiến độ thực hiện của đơn vị nhà thầu.',
    },
]

WHY_US = [
    {
        'icon': 'fa-bullseye',
        'title': 'Độ chính xác >96%',
        'description': 'Mô hình AI được huấn luyện trên hơn 2 triệu ảnh mặt đường thực tế tại Việt Nam, đạt độ chính xác nhận diện vượt tiêu chuẩn ngành.',
    },
    {
        'icon': 'fa-bolt',
        'title': 'Xử lý 60 FPS thời gian thực',
        'description': 'Phân tích video trực tiếp 60 khung hình/giây trên thiết bị Edge AI mà không cần kết nối Internet liên tục ở hiện trường.',
    },
    {
        'icon': 'fa-map-location-dot',
        'title': 'Tích hợp GIS chuẩn VN-2000',
        'description': 'Mọi điểm hư hỏng đều được gán tọa độ chuẩn VN-2000/WGS-84, kết nối trực tiếp vào hệ thống GIS của Sở GTVT.',
    },
    {
        'icon': 'fa-file-invoice',
        'title': 'Báo cáo PDF/Excel tự động',
        'description': 'Xuất báo cáo kiểm định chuẩn PCI/IRI theo quy trình của Tổng cục Đường bộ, giúp tiết kiệm 80% thời gian lập báo cáo.',
    },
    {
        'icon': 'fa-shield-halved',
        'title': 'Tuân thủ tiêu chuẩn quốc tế',
        'description': 'Hệ thống tuân thủ các tiêu chuẩn IRC, AASHTO, WHO và quy chuẩn ngành đường bộ Việt Nam, dễ dàng tích hợp vào hệ thống BMS hiện có.',
    },
    {
        'icon': 'fa-headset',
        'title': 'Hỗ trợ kỹ thuật 24/7',
        'description': 'Đội ngũ kỹ sư TADIC hỗ trợ triển khai, đào tạo vận hành và bảo trì hệ thống xuyên suốt trong toàn bộ vòng đời hợp đồng.',
    },
]

COMPANY_INFO = {
    'name':    'Công ty Cổ phần Xây dựng và Công nghệ TADIC',
    'short':   'TADIC',
    'founded': '2019',
    'address': 'Tầng 4, Tòa nhà LND Galaxy, Số 3 đường Galaxy 6, Phường Hà Đông, TP. Hà Nội',
    'phone':   '(024) 3812 3456',
    'email':   'contact@tadic.vn',
    'website': 'www.tadic.vn',
}


def _base_ctx():
    """Context dùng chung cho tất cả views."""
    return {
        'about_cards':   ABOUT_CARDS,
        'process_steps': PROCESS_STEPS,
        'why_us':        WHY_US,
        'company':       COMPANY_INFO,
    }


# ── Views ─────────────────────────────────────────────────────────────────────

def home(request):
    """Trang chủ — Corporate overview."""
    ctx = _base_ctx()
    ctx.update({
        'products':      Product.objects.filter(is_active=True),
        'stats':         Stat.objects.all(),
        'news_articles': NewsArticle.objects.filter(is_published=True)[:3],
        'projects':      Project.objects.filter(is_active=True)[:4],
        'testimonials':  Testimonial.objects.filter(is_active=True),
        'partners':      Partner.objects.filter(is_active=True),
    })
    return render(request, 'home/index.html', ctx)


def ve_tadic(request):
    """Trang Về TADIC."""
    ctx = _base_ctx()
    ctx.update({
        'stats': Stat.objects.all(),
        'page_title': 'Về TADIC',
    })
    return render(request, 'home/ve_tadic.html', ctx)


def san_pham_list(request):
    """Danh sách sản phẩm và tác nhân AI."""
    ctx = _base_ctx()
    ctx.update({
        'products':      Product.objects.filter(is_active=True),
        'page_title':    'Tác nhân AI',
        'page_desc':     'Hệ sinh thái sản phẩm và tác nhân AI cho quản lý hạ tầng giao thông đường bộ.',
    })
    return render(request, 'home/san_pham.html', ctx)


def san_pham_detail(request, key):
    """Chi tiết sản phẩm."""
    product  = get_object_or_404(Product, key=key, is_active=True)
    related  = Product.objects.filter(
        is_active=True, category_group=product.category_group
    ).exclude(pk=product.pk)[:3]
    ctx = _base_ctx()
    ctx.update({
        'product':    product,
        'related':    related,
        'page_title': product.title,
        'page_desc':  product.subtitle,
    })
    return render(request, 'home/san_pham_detail.html', ctx)


def du_an_list(request):
    """Trang dự án tiêu biểu."""
    ctx = _base_ctx()
    ctx.update({
        'projects':    Project.objects.filter(is_active=True),
        'page_title':  'Dự án tiêu biểu',
        'page_desc':   'Các công trình TADIC đã triển khai thành công trên toàn quốc.',
    })
    return render(request, 'home/du_an.html', ctx)


def tin_tuc_list(request):
    """Danh sách tin tức."""
    ctx = _base_ctx()
    ctx.update({
        'articles':   NewsArticle.objects.filter(is_published=True),
        'page_title': 'Tin tức & Nghiên cứu',
        'page_desc':  'Cập nhật mới nhất về công nghệ AI hạ tầng giao thông và hoạt động TADIC.',
    })
    return render(request, 'home/tin_tuc.html', ctx)


def tin_tuc_detail(request, slug):
    """Chi tiết bài viết."""
    article  = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    related  = NewsArticle.objects.filter(is_published=True).exclude(pk=article.pk)[:3]
    ctx = _base_ctx()
    ctx.update({
        'article':    article,
        'related':    related,
        'page_title': article.title,
        'page_desc':  article.summary,
    })
    return render(request, 'home/tin_tuc_detail.html', ctx)


def lien_he(request):
    """Trang liên hệ."""
    ctx = _base_ctx()
    ctx.update({
        'page_title': 'Liên hệ',
        'page_desc':  'Để lại thông tin — đội ngũ kỹ sư TADIC sẽ liên hệ tư vấn trong 24 giờ.',
    })
    return render(request, 'home/lien_he.html', ctx)
