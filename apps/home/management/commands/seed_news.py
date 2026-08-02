from django.core.management.base import BaseCommand
from home.models import NewsArticle

NEWS = [
    {
        "slug": "news-1",
        "title": "AI và Thị giác máy tính đang thay đổi ngành khảo sát đường bộ ra sao?",
        "date": "2026-06-15",
        "author": "Đội ngũ R&D TADIC",
        "image_url": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=900&q=80",
        "summary": "Từ khảo sát thủ công tốn kém đến thị giác máy tính thời gian thực với độ chính xác trên 96% — hành trình chuyển đổi công nghệ của ngành khảo sát mặt đường.",
        "content": """
      <p>Trước đây, công tác khảo sát chất lượng mặt đường tại Việt Nam chủ yếu dựa vào lực lượng nhân công đi bộ dọc tuyến đường hoặc di chuyển bằng ô tô với tốc độ chậm để quan sát bằng mắt thường. Phương pháp này không chỉ tốn kém thời gian, chi phí mà còn tiềm ẩn nguy cơ mất an toàn giao thông rất lớn cho cán bộ kiểm định.</p>
      <h3>Ứng dụng mô hình học sâu trong phát hiện hư hỏng</h3>
      <p>Sự ra đời của thị giác máy tính thế hệ mới kết hợp mô hình học sâu (Deep Learning) đã hoàn toàn thay đổi cục diện. Hệ thống <strong>Road Vision AI</strong> của TADIC sử dụng các camera chuẩn công nghiệp 4K gắn phía trước xe khảo sát, thu thập hàng ngàn khung hình mỗi giây khi xe di chuyển ở tốc độ thường (50 - 80 km/h).</p>
      <div class="article-highlight">
        "Thuật toán AI tự động phân loại vết nứt dọc, nứt ngang, nứt chân chim và ổ gà với thời gian phản hồi dưới 16ms, độ chính xác nhận diện thực tế đạt tới 96.4%."
      </div>
      <h3>Số hóa dữ liệu gán tọa độ VN-2000</h3>
      <p>Tất cả hình ảnh hư hỏng sau khi được phát hiện đều gán tự động tọa độ vệ tinh GPS RTK độ chính xác milimet. Dữ liệu được đưa thẳng lên bản đồ điện tử GIS, giúp các kỹ sư giao thông dễ dàng tra cứu vị trí hư hỏng trên máy tính hoặc tablet mà không cần phải ra lại hiện trường.</p>
        """,
        "is_published": True,
    },
    {
        "slug": "news-2",
        "title": "Lộ trình số hóa 100% dữ liệu tài sản hạ tầng giao thông đến năm 2030",
        "date": "2026-05-28",
        "author": "Ban Tư vấn Chuyển đổi số TADIC",
        "image_url": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=900&q=80",
        "summary": "Chiến lược xây dựng mô hình Song sinh số (Digital Twin) đường bộ, liên thông dữ liệu từ Trung ương đến địa phương.",
        "content": """
      <p>Quyết định của Chính phủ và Bộ GTVT về Chiến lược Chuyển đổi số ngành Giao thông vận tải đặt ra mục tiêu số hóa toàn bộ hệ thống đường bộ, cầu, hầm và tài sản hạ tầng trên toàn quốc. Việc sở hữu một Cơ sở dữ liệu số tập trung (Digital Twin) là nền tảng cốt lõi cho Đô thị thông minh.</p>
      <h3>Xây dựng mô hình Song sinh số (Digital Twin) đường bộ</h3>
      <p>TADIC đồng hành cùng các Sở GTVT xây dựng mô hình dữ liệu không gian 3D, tích hợp kết quả quét bề mặt từ AI với dữ liệu địa hình GIS. Mỗi cây cầu, biển báo, cọc tiêu, vạch kẻ đường đều trở thành một đối tượng dữ liệu được quản lý tuổi thọ và tình trạng kỹ thuật.</p>
      <div class="article-highlight">
        "Số hóa dữ liệu hạ tầng giúp cơ quan quản lý chuyển từ chiến lược 'hư đâu sửa đó' sang 'bảo trì dự báo', tiết kiệm đáng kể chi phí sửa chữa định kỳ hàng năm."
      </div>
      <h3>Liên thông dữ liệu từ Trung ương đến Địa phương</h3>
      <p>Nền tảng Cloud của TADIC hỗ trợ chuẩn mở RESTful API, cho phép phân quyền truy cập minh bạch cho Cục Đường bộ, Sở GTVT và các nhà thầu quản lý bảo trì.</p>
        """,
        "is_published": True,
    },
    {
        "slug": "news-3",
        "title": "TADIC mở rộng triển khai hệ thống ATS Camera System tại 5 tỉnh thành",
        "date": "2026-05-10",
        "author": "Phòng Dự án ITS TADIC",
        "image_url": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=900&q=80",
        "summary": "Sau thành công tại Hà Nội và TP.HCM, TADIC mở rộng triển khai tới Đà Nẵng, Quảng Ninh, Bình Dương, Đồng Nai và Hải Phòng.",
        "content": """
      <p>Sau giai đoạn thử nghiệm thành công tại Hà Nội và TP. Hồ Chí Minh, TADIC chính thức mở rộng ký kết triển khai hệ thống <strong>ATS Camera System</strong> cho 5 tỉnh thành trọng điểm gồm Đà Nẵng, Quảng Ninh, Bình Dương, Đồng Nai và Hải Phòng.</p>
      <h3>Cảnh báo tức thời sự cố và tắc nghẽn giao thông</h3>
      <p>Hệ thống tích hợp AI edge-computing ngay tại camera, tự động phát hiện các tình huống giao thông nguy hiểm như: ô tô đi ngược chiều, dừng đỗ sai quy định, phương tiện gặp sự cố chết máy giữa đường hay tai nạn giao thông. Cảnh báo lập tức được truyền về Trung tâm Điều hành Giao thông (ITS) trong vòng 2 giây.</p>
      <div class="article-highlight">
        "Tại Quảng Ninh, hệ thống ATS Camera đã hỗ trợ giảm đáng kể thời gian ùn tắc tại các nút giao thông trọng điểm vào giờ cao điểm nhờ khả năng tự động điều tiết chu kỳ đèn tín hiệu."
      </div>
      <h3>Hỗ trợ phân luồng và quy hoạch hạ tầng</h3>
      <p>Dữ liệu đếm lưu lượng xe theo giờ, ngày, tuần giúp các chuyên gia quy hoạch giao thông có cơ sở khoa học chính xác để đề xuất mở rộng làn đường hay điều chỉnh phân luồng giao thông hiệu quả.</p>
        """,
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample news articles"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in NEWS:
            slug = data.pop("slug")
            obj, was_created = NewsArticle.objects.update_or_create(
                slug=slug,
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))
