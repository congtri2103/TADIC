from django.shortcuts import get_object_or_404, redirect, render
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

PRODUCT_VIDEOS = {
    'road-vision-ai': [
        {
            'youtube_id': 'lgg1mVu-1ro',
            'title': 'AI khoanh vùng hư hỏng mặt đường — Camera hành trình phía trước',
            'description': 'Camera trước ghi nhận mặt đường ở tốc độ khảo sát thực tế; mô hình AI khoanh vùng và phân loại hư hỏng trực tiếp trên từng khung hình.',
            'duration': '',
        },
        {
            'youtube_id': 'ZmpErCdjScI',
            'title': 'Quét hiện trạng lề trái tuyến — Camera LHS',
            'description': 'Góc quay hông trái cùng đoạn tuyến, phục vụ đánh giá hiện trạng lề đường, rãnh thoát nước và hệ thống an toàn giao thông.',
            'duration': '',
        },
        {
            'youtube_id': 'Zw1mRAXp_7w',
            'title': 'Quét hiện trạng lề phải tuyến — Camera RHS',
            'description': 'Góc quay hông phải đồng bộ cùng thời điểm với camera trái, cho phép dựng lại hiện trạng đầy đủ hai bên tuyến trong một lượt khảo sát.',
            'duration': '',
        },
        {
            'youtube_id': 'KTRidDrgLRc',
            'title': 'Phân tích liên tục theo hành trình — Đoạn tuyến kế tiếp',
            'description': 'Đoạn khảo sát tiếp theo cho thấy hệ thống nhận diện liên tục, không gián đoạn khi xe di chuyển giữa các phân đoạn tuyến.',
            'duration': '',
        },
    ],
}

VROAD_SOLUTION = {
    'key': 'vroad-ai',
    'name': 'VRoad.AI',
    'tagline': 'Better roads, better future.',
    'summary': 'Nền tảng phần mềm tổng thể quản lý hạ tầng đường bộ, kết nối dữ liệu khảo sát, AI và GIS để biến hiện trạng tuyến đường thành thông tin có thể hành động.',
    'product_keys': [
        'road-vision-ai',
        'road-bound',
        'vegetation-analysis',
        'construction-monitoring',
        'rapid-damage',
        'road-beauty',
    ],
    'modules': [
        {
            'icon': 'fa-chart-pie',
            'name': 'Bảng điều khiển',
            'description': 'Tổng hợp trạng thái tuyến, tài sản, lỗi và chỉ số khảo sát trên một màn hình.',
        },
        {
            'icon': 'fa-boxes-stacked',
            'name': 'Thư viện tài sản',
            'description': 'Tra cứu, phân loại và định vị tài sản dọc tuyến theo dữ liệu khảo sát.',
        },
        {
            'icon': 'fa-triangle-exclamation',
            'name': 'Thư viện lỗi',
            'description': 'Theo dõi mã lỗi, lý trình, mức độ và trạng thái xử lý hiện trường.',
        },
        {
            'icon': 'fa-road-circle-exclamation',
            'name': 'Độ gồ ghề mặt đường',
            'description': 'Trực quan chỉ số IRI trên bản đồ và biểu đồ phân bố theo tuyến.',
        },
        {
            'icon': 'fa-route',
            'name': 'Sổ tuyến đường',
            'description': 'Quản lý hồ sơ tuyến, đoạn tuyến và các thông tin liên quan.',
        },
        {
            'icon': 'fa-cloud-arrow-up',
            'name': 'Tải lên khảo sát',
            'description': 'Tiếp nhận video và dữ liệu khảo sát để xử lý theo từng dự án.',
        },
        {
            'icon': 'fa-photo-film',
            'name': 'Thư viện video',
            'description': 'Tổ chức các phiên video khảo sát theo tuyến và mã phiên.',
        },
        {
            'icon': 'fa-folder-tree',
            'name': 'Dự án',
            'description': 'Quản lý dự án, tuyến và tiến độ khảo sát tập trung.',
        },
        {
            'icon': 'fa-sliders',
            'name': 'Cấu hình hệ thống',
            'description': 'Thiết lập các tham số vận hành và cấu hình nền tảng.',
        },
    ],
}

VROAD_PROBLEM_SOLUTION = {
    'problem': {
        'eyebrow': 'Bài toán',
        'title': 'Hiện trạng đường bộ cần được nhìn thấy đầy đủ hơn',
        'description': 'Dữ liệu tài sản, hư hỏng và chất lượng tuyến thường nằm rời rạc trong nhiều hồ sơ, khó cập nhật liên tục và khó chuyển thành quyết định ưu tiên.',
        'points': [
            'Khảo sát thủ công mất nhiều thời gian và phụ thuộc vào kinh nghiệm.',
            'Dữ liệu hiện trường thiếu liên kết giữa bản đồ, hình ảnh và lý trình.',
            'Đơn vị quản lý khó theo dõi đồng thời tài sản, lỗi và chất lượng mặt đường.',
        ],
    },
    'solution': {
        'eyebrow': 'Lời giải',
        'title': 'Một nền tảng thống nhất cho toàn bộ vòng đời tuyến đường',
        'description': 'VRoad.AI kết nối dữ liệu khảo sát với AI và GIS, giúp đội ngũ quản lý chuyển từ quan sát rời rạc sang một bức tranh hiện trạng có thể truy vấn, phân tích và hành động.',
        'points': [
            'Chuẩn hóa dữ liệu theo dự án, tuyến, lý trình và loại tài sản.',
            'Trực quan hóa kết quả AI trên bản đồ, dashboard và thư viện dữ liệu.',
            'Hỗ trợ lập kế hoạch bảo trì dựa trên bằng chứng từ hiện trường.',
        ],
    },
}

VROAD_SAMPLE_STATS = [
    {'value': '5,20 km', 'label': 'chiều dài khảo sát'},
    {'value': '432', 'label': 'tài sản'},
    {'value': '314', 'label': 'lỗi'},
    {'value': '4,16 m/km', 'label': 'IRI trung bình'},
    {'value': '8,99 m/km', 'label': 'đoạn xấu nhất'},
    {'value': '70,6', 'label': 'PCI (Satisfactory)'},
    {'value': '87,5', 'label': 'PCI (Good)'},
]

VROAD_SAMPLE_NOTE = 'Số liệu từ dự án khảo sát mẫu: Đường Hồ Chí Minh, khảo sát 21/07/2026.'

VROAD_STANDARDS = [
    {
        'icon': 'fa-road',
        'title': 'PCI theo ASTM D6433',
        'description': 'Đánh giá tình trạng mặt đường theo phương pháp PCI được sử dụng trong kiểm định.',
    },
    {
        'icon': 'fa-scale-balanced',
        'title': 'TCVN 14182:2024',
        'description': 'Tham chiếu tiêu chuẩn Việt Nam trong quản lý và khai thác đường bộ.',
    },
    {
        'icon': 'fa-chart-line',
        'title': 'IRI theo dải HDM-4',
        'description': 'Theo dõi độ gồ ghề mặt đường bằng chỉ số IRI theo dải HDM-4.',
    },
]

VROAD_DAMAGE_TYPES = [
    'Nứt da cá sấu (nứt mỏi)',
    'Vá mặt đường',
    'Ổ gà',
    'Vạch kẻ đường bị phai',
    'Biển báo tầm nhìn kém',
    'Hư hỏng biển báo / kết cấu biển báo',
    'Hư hỏng gạch lát vỉa hè',
    'Hư hỏng gờ giảm tốc',
    'Thiếu tấm đậy cống',
]

VROAD_ASSET_GROUPS = [
    'Biển báo chỉ dẫn',
    'Hệ thống giao thông thông minh (ITS)',
    'Chiếu sáng đường bộ',
    'Mặt đường',
    'Tài sản hạ tầng khác (OIA)',
]

VROAD_UI_IMAGES = [
    {'path': 'images/vroad/dashboard-tai-san.webp', 'title': 'Bảng điều khiển tài sản', 'alt': 'Bảng điều khiển VRoad.AI với dữ liệu tuyến, tài sản và lỗi', 'width': 1323, 'height': 640},
    {'path': 'images/vroad/chi-tiet-hu-hong.webp', 'title': 'Chi tiết hư hỏng', 'alt': 'So sánh khung hình gốc và khung hình đã được AI phân tích', 'width': 952, 'height': 555},
    {'path': 'images/vroad/thu-vien-loi.webp', 'title': 'Thư viện lỗi', 'alt': 'Bản đồ và danh sách lỗi có mã lỗi, lý trình', 'width': 1344, 'height': 647},
    {'path': 'images/vroad/thu-vien-tai-san.webp', 'title': 'Thư viện tài sản', 'alt': 'Bản đồ và danh sách tài sản có mã tài sản', 'width': 1358, 'height': 655},
    {'path': 'images/vroad/dashboard-hu-hong.webp', 'title': 'Dashboard hư hỏng', 'alt': 'Dashboard phân tích hư hỏng theo mức độ', 'width': 1304, 'height': 616},
    {'path': 'images/vroad/iri-01.webp', 'title': 'Phân tích IRI', 'alt': 'Bản đồ và biểu đồ phân tích độ gồ ghề IRI', 'width': 1347, 'height': 654},
    {'path': 'images/vroad/iri-02.webp', 'title': 'Màn hình IRI bổ sung', 'alt': 'Màn hình bổ sung của phân hệ phân tích IRI', 'width': 1327, 'height': 642},
    {'path': 'images/vroad/iri-03.webp', 'title': 'Biểu đồ IRI', 'alt': 'Biểu đồ và dữ liệu phân bố IRI theo tuyến', 'width': 1335, 'height': 647},
    {'path': 'images/vroad/thu-vien-video.webp', 'title': 'Thư viện video', 'alt': 'Lưới các phiên video khảo sát trong VRoad.AI', 'width': 1323, 'height': 645},
    {'path': 'images/vroad/hang-doi-video.webp', 'title': 'Hàng đợi video', 'alt': 'Hàng đợi xử lý video khảo sát', 'width': 1312, 'height': 657},
    {'path': 'images/vroad/tao-du-an.webp', 'title': 'Tạo dự án', 'alt': 'Biểu mẫu tạo dự án khảo sát', 'width': 1347, 'height': 674},
    {'path': 'images/vroad/tao-tuyen-01.webp', 'title': 'Tạo tuyến', 'alt': 'Biểu mẫu tạo tuyến có bản đồ', 'width': 1204, 'height': 586},
    {'path': 'images/vroad/tao-tuyen-02.webp', 'title': 'Thông tin tuyến', 'alt': 'Màn hình thông tin tuyến và bản đồ', 'width': 1353, 'height': 635},
    {'path': 'images/vroad/cau-hinh-he-thong.webp', 'title': 'Cấu hình hệ thống', 'alt': 'Màn hình cấu hình hệ thống VRoad.AI', 'width': 1302, 'height': 656},
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
        'solution':      VROAD_SOLUTION,
        'sample_stats':  VROAD_SAMPLE_STATS,
        'sample_note':   VROAD_SAMPLE_NOTE,
        'nav_solutions': Product.objects.filter(is_active=True, kind='solution'),
        'nav_products':  Product.objects.filter(is_active=True, kind='product'),
    }


# ── Views ─────────────────────────────────────────────────────────────────────

def home(request):
    """Trang chủ — Corporate overview."""
    ctx = _base_ctx()
    ctx.update({
        'solutions':     Product.objects.filter(is_active=True, kind='solution'),
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


def giai_phap_list(request):
    """Danh sách các giải pháp AI chuyên biệt."""
    ctx = _base_ctx()
    ctx.update({
        'products':   Product.objects.filter(is_active=True, kind='solution'),
        'page_title': 'Giải pháp AI',
        'page_desc':  'Hệ sinh thái giải pháp AI cho quản lý hạ tầng giao thông đường bộ.',
    })
    return render(request, 'home/giai_phap_list.html', ctx)


def san_pham_list(request):
    """Danh sách các sản phẩm thương mại của TADIC."""
    ctx = _base_ctx()
    ctx.update({
        'products':   Product.objects.filter(is_active=True, kind='product'),
        'page_title': 'Sản phẩm',
        'page_desc':  'Các sản phẩm thương mại ứng dụng AI và số hóa của TADIC.',
    })
    return render(request, 'home/san_pham.html', ctx)


def san_pham_vroad(request):
    """Trang giới thiệu sản phẩm nền tảng VRoad.AI."""
    products_by_key = {
        product.key: product
        for product in Product.objects.filter(
            is_active=True,
            key__in=VROAD_SOLUTION['product_keys'],
        )
    }
    solution_products = [
        products_by_key[key]
        for key in VROAD_SOLUTION['product_keys']
        if key in products_by_key
    ]
    ctx = _base_ctx()
    ctx.update({
        'page_title': VROAD_SOLUTION['name'],
        'page_desc': VROAD_SOLUTION['summary'],
        'solution_products': solution_products,
        'problem_solution': VROAD_PROBLEM_SOLUTION,
        'sample_stats': VROAD_SAMPLE_STATS,
        'sample_note': VROAD_SAMPLE_NOTE,
        'standards': VROAD_STANDARDS,
        'damage_types': VROAD_DAMAGE_TYPES,
        'asset_groups': VROAD_ASSET_GROUPS,
        'ui_images': VROAD_UI_IMAGES,
    })
    return render(request, 'home/san_pham_vroad.html', ctx)


def _product_detail(request, key, expected_kind):
    product = get_object_or_404(Product, key=key, is_active=True)
    if product.kind != expected_kind:
        return redirect(product.get_absolute_url(), permanent=True)

    related = Product.objects.filter(
        is_active=True,
        kind=product.kind,
        category_group=product.category_group,
    ).exclude(pk=product.pk)[:3]
    ctx = _base_ctx()
    ctx.update({
        'product': product,
        'related': related,
        'videos': PRODUCT_VIDEOS.get(key, []),
        'is_vroad_product': key in VROAD_SOLUTION['product_keys'],
        'page_title': product.title,
        'page_desc': product.subtitle,
    })
    return render(request, 'home/san_pham_detail.html', ctx)


def giai_phap_detail(request, key):
    """Chi tiết giải pháp AI; chuyển hướng nếu key thuộc danh mục sản phẩm."""
    return _product_detail(request, key, 'solution')


def san_pham_detail(request, key):
    """Chi tiết sản phẩm; chuyển hướng nếu key thuộc danh mục giải pháp."""
    return _product_detail(request, key, 'product')


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
