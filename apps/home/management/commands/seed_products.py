from django.core.management.base import BaseCommand
from home.models import Product

PRODUCTS = [
    # ── Road Network Monitoring ──
    {
        "key": "road-vision-ai",
        "title": "Đặc vụ Tình trạng Mặt đường",
        "subtitle": "Phân tích hình ảnh & video mặt đường theo thời gian thực",
        "icon": "fa-road-circle-exclamation",
        "tag": "Giám sát đường bộ",
        "category_group": "road_network",
        "status": "live",
        "order": 1,
        "description": "Đánh giá tình trạng mặt đường tự động theo tiêu chuẩn IRC, MoRTH, ASTM, AASHTO, PAS và quy trình nội bộ. Phát hiện, phân loại 15+ loại khuyết tật mặt đường với độ chính xác >96%.",
        "features": [
            "Nhận diện 15+ loại hư hỏng: Vết nứt dọc, nứt ngang, nứt lưới, ổ gà, lún rãnh, bong tróc.",
            "Đo đạc chính xác diện tích (m²) và độ rộng nứt (mm) thời gian thực.",
            "Tích hợp GPS RTK gán tọa độ chuẩn VN-2000 cho từng điểm hư hỏng.",
            "Tốc độ xử lý video đến 60 FPS trên thiết bị Edge AI ngoại trường."
        ],
    },
    {
        "key": "road-bound",
        "title": "Đại lý Kiểm kê Ven đường",
        "subtitle": "Nền tảng định vị & Quản lý ranh giới hành lang an toàn giao thông",
        "icon": "fa-signs-post",
        "tag": "Kiểm kê tài sản",
        "category_group": "road_network",
        "status": "live",
        "order": 2,
        "description": "Theo dõi và đánh giá biển báo, rào chắn và tài sản ven đường với độ chính xác kỹ thuật. Tự động hóa việc trích xuất và định vị vào bản đồ GIS số tập trung.",
        "features": [
            "Khoanh vùng tự động ranh giới giải phóng mặt bằng và hành lang an toàn.",
            "Tự động so sánh dữ liệu thực địa để phát hiện công trình lấn chiếm trái phép.",
            "Truy xuất lịch sử biến động sử dụng đất theo từng mốc thời gian.",
            "Xuất dữ liệu chuẩn GIS (Shapefile, GeoJSON, KML) kết nối phần mềm ngành GTVT."
        ],
    },
    {
        "key": "vegetation-analysis",
        "title": "Đặc vụ Phân tích Thảm thực vật",
        "subtitle": "Giám sát thảm thực vật ven đường bằng AI",
        "icon": "fa-leaf",
        "tag": "Giám sát đường bộ",
        "category_group": "road_network",
        "status": "live",
        "order": 3,
        "description": "Giám sát thảm thực vật ven đường vì mục tiêu an toàn và tuân thủ tiêu chuẩn đường xanh (Green Highway) bằng dữ liệu camera hành trình và vệ tinh.",
        "features": [
            "Phát hiện thảm thực vật xâm lấn hành lang an toàn đường bộ.",
            "Đánh giá mức độ che phủ và loại thực vật ven đường.",
            "Tích hợp dữ liệu đa thời điểm để theo dõi biến động theo mùa.",
            "Cảnh báo sớm các khu vực có nguy cơ cháy rừng ven đường."
        ],
    },
    {
        "key": "construction-monitoring",
        "title": "Đặc vụ Giám sát Thi công",
        "subtitle": "Theo dõi tiến độ và chất lượng thi công đường bộ",
        "icon": "fa-hard-hat",
        "tag": "Giám sát đường bộ",
        "category_group": "road_network",
        "status": "beta",
        "order": 4,
        "description": "Theo dõi tiến độ thi công đường bộ, phát hiện sai lệch so với thiết kế và đánh giá chất lượng dự án bằng AI từ dữ liệu drone, vệ tinh và camera công trường.",
        "features": [
            "So sánh tiến độ thực tế với kế hoạch thi công tự động.",
            "Phát hiện sai lệch kết cấu so với bản vẽ thiết kế.",
            "Đánh giá chất lượng thi công mặt đường và lớp móng.",
            "Tích hợp dữ liệu từ nhiều nguồn: drone, vệ tinh, camera công trường."
        ],
    },
    {
        "key": "rapid-damage",
        "title": "Đặc vụ Đánh giá Hư hỏng Nhanh",
        "subtitle": "Đánh giá thiệt hại đường bộ sau thiên tai bằng AI",
        "icon": "fa-satellite",
        "tag": "Giám sát đường bộ",
        "category_group": "road_network",
        "status": "beta",
        "order": 5,
        "description": "Sử dụng ảnh vệ tinh và trí tuệ nhân tạo để đánh giá nhanh thiệt hại đường bộ sau thiên tai, hỗ trợ ưu tiên nguồn lực cứu hộ và lập kế hoạch khắc phục.",
        "features": [
            "Phân tích ảnh vệ tinh trước/sau thiên tai để đánh giá mức độ hư hỏng.",
            "Phân loại mức độ thiệt hại: nhẹ, trung bình, nghiêm trọng.",
            "Ước tính chi phí khắc phục và nguồn lực cần thiết.",
            "Tích hợp bản đồ GIS để khoanh vùng khu vực ưu tiên xử lý."
        ],
    },
    {
        "key": "road-beauty",
        "title": "Đặc vụ Vệ sinh & Mỹ quan",
        "subtitle": "Giám sát vệ sinh đô thị và mỹ quan đường phố",
        "icon": "fa-broom",
        "tag": "Giám sát đường bộ",
        "category_group": "road_network",
        "status": "beta",
        "order": 6,
        "description": "Giám sát vệ sinh, mỹ quan đô thị và các chỉ số chất lượng môi trường ven đường bằng AI. Phát hiện điểm rác thải và đánh giá mỹ quan đường phố.",
        "features": [
            "Phát hiện điểm rác thải và đánh giá mức độ ô nhiễm ven đường.",
            "Kiểm tra tình trạng biển báo, cột đèn và các công trình mỹ quan.",
            "Đánh giá điểm số mỹ quan đường phố theo tiêu chuẩn đô thị văn minh.",
            "Gợi ý lịch dọn dẹp và bảo trì định kỳ dựa trên dữ liệu thực tế."
        ],
    },
    # ── Road Safety ──
    {
        "key": "ats-camera",
        "title": "Tác nhân Phân tích Lưu lượng",
        "subtitle": "Hệ thống camera AI giám sát giao thông thông minh 24/7",
        "icon": "fa-car-burst",
        "tag": "An toàn giao thông",
        "category_group": "road_safety",
        "status": "live",
        "order": 7,
        "description": "Tự động đếm phương tiện, phân loại giao thông và phân tích ùn tắc cho quy hoạch và tối ưu hóa. Biến camera CCTV thông thường thành cảm biến giao thông thông minh.",
        "features": [
            "Đếm lưu lượng và phân loại 8 nhóm phương tiện (Xe máy, ô tô, xe tải, container...).",
            "Đo tốc độ di chuyển trung bình và nhận diện hành vi vi phạm giao thông.",
            "Cảnh báo tức thời sự cố tắc nghẽn, tai nạn, xe dừng đỗ trái phép.",
            "Vận hành ổn định trong điều kiện thời tiết xấu và ban đêm."
        ],
    },
    {
        "key": "blackspot-analysis",
        "title": "Tác nhân Phân tích Điểm đen",
        "subtitle": "Xác định và phân tích khu vực tiềm ẩn tai nạn giao thông",
        "icon": "fa-location-crosshairs",
        "tag": "An toàn giao thông",
        "category_group": "road_safety",
        "status": "live",
        "order": 8,
        "description": "Xác định chính xác các điểm đen tai nạn giao thông dựa trên dữ liệu lịch sử tai nạn, đặc điểm hình học đường bộ và lưu lượng giao thông.",
        "features": [
            "Phân tích dữ liệu tai nạn giao thông đa năm.",
            "Xác định nguyên nhân gốc rễ của từng điểm đen.",
            "Đề xuất giải pháp kỹ thuật và ước tính hiệu quả giảm tai nạn.",
            "Theo dõi hiệu quả can thiệp sau khi cải tạo."
        ],
    },
    {
        "key": "road-safety-audit",
        "title": "Tác nhân Kiểm toán An toàn",
        "subtitle": "Kiểm toán an toàn đường bộ tự động hóa",
        "icon": "fa-clipboard-list",
        "tag": "An toàn giao thông",
        "category_group": "road_safety",
        "status": "beta",
        "order": 9,
        "description": "Kiểm toán an toàn đường bộ tự động ở các giai đoạn thiết kế, thi công và vận hành — tuân thủ tiêu chuẩn IRC, AASHTO và WHO.",
        "features": [
            "Kiểm toán an toàn ở giai đoạn thiết kế: phát hiện bất cập về tầm nhìn, độ dốc, khúc cua nguy hiểm.",
            "Kiểm toán giai đoạn vận hành: phát hiện hư hỏng công trình an toàn.",
            "Chấm điểm an toàn cho từng đoạn tuyến theo tiêu chuẩn quốc tế.",
            "Đề xuất giải pháp cải tạo điểm đen kèm dự toán chi phí."
        ],
    },
    {
        "key": "anpr",
        "title": "Tác nhân Nhận diện Biển số",
        "subtitle": "Nhận diện và theo dõi biển số phương tiện thời gian thực",
        "icon": "fa-camera-cctv",
        "tag": "An toàn giao thông",
        "category_group": "road_safety",
        "status": "live",
        "order": 10,
        "description": "Phát hiện, đọc và theo dõi biển số phương tiện từ luồng video trực tiếp với độ chính xác cao, hỗ trợ biển số Việt Nam và quốc tế.",
        "features": [
            "Nhận diện biển số với độ chính xác >97% trong điều kiện thực tế.",
            "Hỗ trợ tất cả các loại biển số Việt Nam và quốc tế.",
            "Tra cứu thông tin phương tiện và cảnh báo xe vi phạm.",
            "Lưu trữ lịch sử di chuyển và xuất báo cáo thống kê."
        ],
    },
    {
        "key": "facial-recognition",
        "title": "Tác nhân Nhận diện Khuôn mặt",
        "subtitle": "Giám sát và nhận diện nhân sự trong môi trường hạ tầng",
        "icon": "fa-face-smile",
        "tag": "An toàn giao thông",
        "category_group": "road_safety",
        "status": "beta",
        "order": 11,
        "description": "Nhận diện, theo dõi và giám sát sự hiện diện của nhân sự trong các khu vực thi công và môi trường hạ tầng giao thông.",
        "features": [
            "Nhận diện và định danh nhân sự từ luồng video trực tiếp.",
            "Cảnh báo khi nhân sự không được phép vào khu vực hạn chế.",
            "Đếm số lượng và theo dõi thời gian làm việc của công nhân.",
            "Tích hợp với hệ thống chấm công và quản lý an toàn lao động."
        ],
    },
    # ── Workflow Automation ──
    {
        "key": "ai-inspection",
        "title": "Tác nhân DMS & Báo cáo",
        "subtitle": "Nền tảng lập báo cáo kiểm định & Quản lý bảo trì tự động",
        "icon": "fa-file-contract",
        "tag": "Quy trình tự động",
        "category_group": "workflow",
        "status": "live",
        "order": 12,
        "description": "Tự động hóa quy trình kỹ thuật và tài sản với khả năng truy xuất Thiết kế–Hoàn công–Bảo trì. Tính toán chỉ số PCI và xuất báo cáo kiểm định tự động.",
        "features": [
            "Tự động tính toán chỉ số PCI, IRI theo quy chuẩn ngành đường bộ Việt Nam.",
            "Xuất báo cáo kiểm định chất lượng mặt đường dạng PDF/Excel chuẩn ISO.",
            "Gợi ý phương án sửa chữa tối ưu (trám nứt, cào bóc, thảm lại) kèm dự toán kinh phí.",
            "Quản lý tiến độ khắc phục hư hỏng của các đơn vị nhà thầu bảo trì."
        ],
    },
    {
        "key": "tender-intelligence",
        "title": "Tác nhân Đấu thầu & Hồ sơ",
        "subtitle": "Theo dõi và hỗ trợ chuẩn bị hồ sơ đấu thầu",
        "icon": "fa-gavel",
        "tag": "Quy trình tự động",
        "category_group": "workflow",
        "status": "live",
        "order": 13,
        "description": "Theo dõi tự động các gói thầu trên toàn quốc, trích xuất thông số kỹ thuật và hỗ trợ tạo hồ sơ dự thầu với AI.",
        "features": [
            "Theo dõi và tổng hợp thông tin gói thầu từ nhiều nguồn.",
            "Trích xuất tự động yêu cầu kỹ thuật và tiêu chí đánh giá.",
            "Hỗ trợ soạn thảo hồ sơ dự thầu với đề xuất nội dung AI.",
            "Cảnh báo hạn chót nộp hồ sơ và các yêu cầu bổ sung."
        ],
    },
    {
        "key": "contract-intelligence",
        "title": "Tác nhân Quản lý Hợp đồng",
        "subtitle": "Rà soát và quản lý hợp đồng xây dựng thông minh",
        "icon": "fa-scale-balanced",
        "tag": "Quy trình tự động",
        "category_group": "workflow",
        "status": "live",
        "order": 14,
        "description": "Rà soát hợp đồng xây dựng bằng AI, xác định rủi ro pháp lý và hỗ trợ quản lý khiếu nại. Tích hợp quy trình phê duyệt tập trung.",
        "features": [
            "Rà soát hợp đồng tự động, phát hiện điều khoản rủi ro.",
            "So sánh điều khoản giữa các phiên bản hợp đồng.",
            "Hỗ trợ quản lý khiếu nại và tranh chấp hợp đồng.",
            "Lưu trữ và tra cứu hợp đồng thông minh với AI Search."
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the database with 14 AI agent products"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in PRODUCTS:
            key = data.pop("key")
            features = data.pop("features")
            obj, was_created = Product.objects.update_or_create(
                key=key,
                defaults={**data, "features": features},
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))
