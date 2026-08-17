"""
Management command: seed_data
Seed dữ liệu thật cho: NewsArticle, Project, Testimonial, Partner, Stat
Chạy: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from home.models import NewsArticle, Project, Testimonial, Partner, Stat
from datetime import date


# ─── News Articles ────────────────────────────────────────────────────────────
NEWS = [
    {
        "slug": "ai-computer-vision-khao-sat-duong-bo",
        "title": "AI và Thị giác máy tính đang thay đổi ngành khảo sát đường bộ ra sao?",
        "date": date(2026, 6, 15),
        "author": "Đội ngũ R&D TADIC",
        "image_url": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=900&q=80",
        "summary": "Từ nhân công đi bộ dọc tuyến đến camera AI 4K xử lý 60 FPS — công nghệ thị giác máy tính đang cách mạng hóa hoàn toàn công tác kiểm định mặt đường tại Việt Nam.",
        "content": """<p>Trước đây, công tác khảo sát chất lượng mặt đường tại Việt Nam chủ yếu dựa vào lực lượng nhân công đi bộ dọc tuyến đường hoặc di chuyển bằng ô tô với tốc độ chậm để quan sát bằng mắt thường. Phương pháp này không chỉ tốn kém thời gian, chi phí mà còn tiềm ẩn nguy cơ mất an toàn giao thông rất lớn cho cán bộ kiểm định.</p>
<h3>Ứng dụng mô hình Deep Learning YOLOv8 trong phát hiện hư hỏng</h3>
<p>Sự ra đời của thị giác máy tính thế hệ mới kết hợp mô hình học sâu (Deep Learning) đã hoàn toàn thay đổi cục diện. Hệ thống <strong>Road Vision AI</strong> của TADIC sử dụng các camera chuẩn công nghiệp 4K gắn phía trước xe khảo sát, thu thập hàng ngàn khung hình mỗi giây khi xe di chuyển ở tốc độ thường (50–80 km/h).</p>
<div class="article-highlight">"Thuật toán AI tự động phân loại vết nứt dọc, nứt ngang, nứt chân chim và ổ gà với thời gian phản hồi dưới 16ms, độ chính xác nhận diện thực tế đạt tới 96,4%."</div>
<h3>Số hóa dữ liệu gán tọa độ VN-2000</h3>
<p>Tất cả hình ảnh hư hỏng sau khi được phát hiện đều gán tự động tọa độ vệ tinh GPS RTK độ chính xác milimet. Dữ liệu được đưa thẳng lên bản đồ điện tử GIS, giúp các kỹ sư giao thông dễ dàng tra cứu vị trí hư hỏng trên máy tính hoặc tablet mà không cần phải ra lại hiện trường.</p>""",
        "is_published": True,
    },
    {
        "slug": "lo-trinh-so-hoa-tai-san-ha-tang-giao-thong-2030",
        "title": "Lộ trình số hóa 100% dữ liệu tài sản hạ tầng giao thông đến năm 2030",
        "date": date(2026, 5, 28),
        "author": "Ban Tư vấn Chuyển đổi số TADIC",
        "image_url": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=900&q=80",
        "summary": "Chiến lược chuyển đổi số ngành GTVT đặt mục tiêu số hóa toàn bộ hệ thống đường bộ, cầu và hầm. TADIC đồng hành cùng Sở GTVT xây dựng Digital Twin hạ tầng quốc gia.",
        "content": """<p>Quyết định của Chính phủ và Bộ GTVT về Chiến lược Chuyển đổi số ngành Giao thông vận tải đặt ra mục tiêu số hóa toàn bộ hệ thống đường bộ, cầu, hầm và tài sản hạ tầng trên toàn quốc. Việc sở hữu một Cơ sở dữ liệu số tập trung (Digital Twin) là nền tảng cốt lõi cho Đô thị thông minh.</p>
<h3>Xây dựng mô hình Song sinh số (Digital Twin) đường bộ</h3>
<p>TADIC đồng hành cùng các Sở GTVT xây dựng mô hình dữ liệu không gian 3D, tích hợp kết quả quét bề mặt từ AI với dữ liệu địa hình GIS. Mỗi cây cầu, biển báo, cọc tiêu, vạch kẻ đường đều trở thành một đối tượng dữ liệu được quản lý tuổi thọ và tình trạng kỹ thuật.</p>
<div class="article-highlight">"Số hóa dữ liệu hạ tầng giúp cơ quan quản lý chuyển từ chiến lược 'hư đâu sửa đó' sang 'bảo trì dự báo', tiết kiệm tới 40% chi phí sửa chữa định kỳ hàng năm."</div>
<h3>Liên thông dữ liệu từ Trung ương đến Địa phương</h3>
<p>Nền tảng Cloud của TADIC hỗ trợ chuẩn mở RESTful API, cho phép phân quyền truy cập minh bạch cho Cục Đường bộ, Sở GTVT và các nhà thầu quản lý bảo trì. Lộ trình đặt mục tiêu hoàn thành số hóa 100% tài sản hạ tầng quốc lộ vào năm 2028 và tỉnh lộ vào năm 2030.</p>""",
        "is_published": True,
    },
    {
        "slug": "tadic-trien-khai-ats-camera-5-tinh-thanh",
        "title": "TADIC mở rộng triển khai hệ thống ATS Camera System tại 5 tỉnh thành",
        "date": date(2026, 5, 10),
        "author": "Phòng Dự án ITS TADIC",
        "image_url": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=900&q=80",
        "summary": "Sau giai đoạn thử nghiệm thành công tại Hà Nội và TP. HCM, TADIC mở rộng ký kết ATS Camera System cho 5 tỉnh: Đà Nẵng, Quảng Ninh, Bình Dương, Đồng Nai và Hải Phòng.",
        "content": """<p>Sau giai đoạn thử nghiệm thành công tại Hà Nội và TP. Hồ Chí Minh, TADIC chính thức mở rộng ký kết triển khai hệ thống <strong>ATS Camera System</strong> cho 5 tỉnh thành trọng điểm gồm Đà Nẵng, Quảng Ninh, Bình Dương, Đồng Nai và Hải Phòng.</p>
<h3>Cảnh báo tức thời sự cố và tắc nghẽn giao thông</h3>
<p>Hệ thống tích hợp AI edge-computing ngay tại camera, tự động phát hiện các tình huống giao thông nguy hiểm như: ô tô đi ngược chiều, dừng đỗ sai quy định, phương tiện gặp sự cố chết máy giữa đường hay tai nạn giao thông. Cảnh báo lập tức được truyền về Trung tâm Điều hành Giao thông (ITS) trong vòng 2 giây.</p>
<div class="article-highlight">"Tại Quảng Ninh, hệ thống ATS Camera đã hỗ trợ giảm 35% thời gian ùn tắc tại các nút giao thông trọng điểm vào giờ cao điểm nhờ khả năng tự động điều tiết chu kỳ đèn tín hiệu."</div>
<h3>Hỗ trợ phân luồng và quy hoạch hạ tầng</h3>
<p>Dữ liệu đếm lưu lượng xe theo giờ, ngày, tuần giúp các chuyên gia quy hoạch giao thông có cơ sở khoa học chính xác để đề xuất mở rộng làn đường hay điều chỉnh phân luồng giao thông hiệu quả.</p>""",
        "is_published": True,
    },
]


# ─── Projects ─────────────────────────────────────────────────────────────────
PROJECTS = [
    {
        "title": "Khảo sát Cao tốc Bắc–Nam (Đoạn Hà Nội – Đà Nẵng)",
        "description": "Triển khai hệ thống Road Vision AI khảo sát toàn tuyến Cao tốc Bắc–Nam đoạn Hà Nội – Đà Nẵng, tổng chiều dài hơn 560 km. Hệ thống phát hiện và phân loại hư hỏng mặt đường, tự động lập bản đồ nhiệt và báo cáo PCI đề xuất phương án bảo trì.",
        "image_url": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=900&q=80",
        "tags": "Road Vision AI, GIS, PCI, Cao tốc",
        "order": 1,
        "is_active": True,
    },
    {
        "title": "Giám sát Quốc lộ 1A — Đà Nẵng đến Quảng Ngãi",
        "description": "Dự án số hóa toàn bộ tài sản hạ tầng và đánh giá tình trạng mặt đường trên 130 km Quốc lộ 1A. Kết quả được tích hợp trực tiếp vào hệ thống GIS của Sở GTVT Đà Nẵng và Quảng Ngãi, phục vụ lập kế hoạch bảo trì năm 2026–2027.",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=900&q=80",
        "tags": "Road Vision AI, Kiểm kê tài sản, GIS, Quốc lộ",
        "order": 2,
        "is_active": True,
    },
    {
        "title": "ATS Camera System — Nút giao Trung tâm Hà Nội",
        "description": "Lắp đặt và vận hành 48 camera AI tại 12 nút giao thông trọng điểm ở trung tâm Hà Nội. Hệ thống tự động đếm lưu lượng, phân loại phương tiện, phát hiện vi phạm và kết nối với Trung tâm Điều hành Giao thông Đô thị Hà Nội (TOC).",
        "image_url": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=900&q=80",
        "tags": "ATS Camera, ITS, Giao thông đô thị, Hà Nội",
        "order": 3,
        "is_active": True,
    },
    {
        "title": "Số hóa Hạ tầng Cầu Thuận Phước — Đà Nẵng",
        "description": "Kiểm định và số hóa toàn bộ kết cấu Cầu Thuận Phước dài 1.856m bằng công nghệ quét 3D LiDAR kết hợp AI. Xây dựng hồ sơ Digital Twin cầu, bao gồm lịch sử bảo trì, tình trạng kết cấu và kế hoạch sửa chữa định kỳ tích hợp với phần mềm BMS.",
        "image_url": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=900&q=80",
        "tags": "Digital Twin, LiDAR, BMS, Cầu đường",
        "order": 4,
        "is_active": True,
    },
]


# ─── Testimonials ─────────────────────────────────────────────────────────────
TESTIMONIALS = [
    {
        "quote": "Hệ thống Road Vision AI của TADIC đã rút ngắn thời gian khảo sát định kỳ trên tuyến vành đai của chúng tôi từ 3 tuần xuống còn 4 ngày, đồng thời báo cáo tự động giúp đội ngũ kỹ thuật tập trung vào phân tích thay vì thu thập số liệu.",
        "author_name": "KS. Nguyễn Văn Minh",
        "author_title": "Trưởng phòng Quản lý Kết cấu Hạ tầng — Sở GTVT Hà Nội",
        "order": 1,
        "is_active": True,
    },
    {
        "quote": "TADIC là đối tác công nghệ tin cậy trong dự án khảo sát Cao tốc Bắc–Nam. Độ chính xác phát hiện hư hỏng vượt yêu cầu kỹ thuật, dữ liệu GIS tích hợp liền mạch vào hệ thống quản lý tài sản của chúng tôi.",
        "author_name": "TS. Trần Thị Lan Anh",
        "author_title": "Phó Giám đốc — Ban QLDA Đầu tư Xây dựng các Công trình Giao thông",
        "order": 2,
        "is_active": True,
    },
    {
        "quote": "ATS Camera System giúp chúng tôi có dữ liệu lưu lượng xe theo thời gian thực trên toàn bộ tuyến Điện Biên Phủ. Đây là nền tảng dữ liệu quan trọng cho đề án quy hoạch giao thông đô thị Đà Nẵng đến 2030.",
        "author_name": "KS. Phạm Quốc Hùng",
        "author_title": "Giám đốc Trung tâm Điều hành Giao thông — Sở GTVT Đà Nẵng",
        "order": 3,
        "is_active": True,
    },
]


# ─── Partners ─────────────────────────────────────────────────────────────────
PARTNERS = [
    {"name": "Bộ Giao thông Vận tải",      "icon_class": "fa-landmark",       "order": 1, "is_active": True},
    {"name": "Tổng Cục Đường bộ VN",        "icon_class": "fa-road",           "order": 2, "is_active": True},
    {"name": "Sở GTVT Hà Nội",             "icon_class": "fa-city",           "order": 3, "is_active": True},
    {"name": "Sở GTVT TP. Hồ Chí Minh",   "icon_class": "fa-city",           "order": 4, "is_active": True},
    {"name": "Sở GTVT Đà Nẵng",            "icon_class": "fa-building",       "order": 5, "is_active": True},
    {"name": "Ban QLDA Thăng Long",        "icon_class": "fa-hard-hat",       "order": 6, "is_active": True},
]


# ─── Stats ────────────────────────────────────────────────────────────────────
STATS = [
    {"label": "km đường đã khảo sát",           "target_value": 1800, "suffix": "+",  "icon": "fa-road",             "order": 1},
    {"label": "Sản phẩm & tác nhân AI trong hệ sinh thái", "target_value": 14, "suffix": "", "icon": "fa-robot", "order": 2},
    {"label": "Độ chính xác nhận diện",          "target_value": 96,   "suffix": "%",  "icon": "fa-bullseye",         "order": 3},
    {"label": "Tỉnh thành đang triển khai",      "target_value": 5,    "suffix": "+",  "icon": "fa-map-location-dot", "order": 4},
]


class Command(BaseCommand):
    help = "Seed NewsArticle, Project, Testimonial, Partner, Stat với dữ liệu thật của TADIC"

    def handle(self, *args, **options):
        self.stdout.write("=== Bắt đầu seed dữ liệu TADIC ===\n")

        # ── News ──
        news_created = news_updated = 0
        for data in NEWS:
            slug = data.pop("slug")
            obj, created = NewsArticle.objects.update_or_create(
                slug=slug, defaults=data
            )
            data["slug"] = slug  # restore for idempotency
            if created:
                news_created += 1
            else:
                news_updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"  NewsArticle  — Created: {news_created}, Updated: {news_updated}"
        ))

        # ── Projects ──
        proj_created = proj_updated = 0
        for data in PROJECTS:
            title = data["title"]
            obj, created = Project.objects.update_or_create(
                title=title, defaults=data
            )
            if created:
                proj_created += 1
            else:
                proj_updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"  Project      — Created: {proj_created}, Updated: {proj_updated}"
        ))

        # ── Testimonials ──
        test_created = test_updated = 0
        for data in TESTIMONIALS:
            author = data["author_name"]
            obj, created = Testimonial.objects.update_or_create(
                author_name=author, defaults=data
            )
            if created:
                test_created += 1
            else:
                test_updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"  Testimonial  — Created: {test_created}, Updated: {test_updated}"
        ))

        # ── Partners ──
        part_created = part_updated = 0
        for data in PARTNERS:
            name = data["name"]
            obj, created = Partner.objects.update_or_create(
                name=name, defaults=data
            )
            if created:
                part_created += 1
            else:
                part_updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"  Partner      — Created: {part_created}, Updated: {part_updated}"
        ))

        # ── Stats ──
        stat_created = stat_updated = 0
        for data in STATS:
            label = data["label"]
            obj, created = Stat.objects.update_or_create(
                label=label, defaults=data
            )
            if created:
                stat_created += 1
            else:
                stat_updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"  Stat         — Created: {stat_created}, Updated: {stat_updated}"
        ))

        self.stdout.write(self.style.SUCCESS("\n=== Seed hoàn thành! ==="))
