from django.core.management.base import BaseCommand
from home.models import Testimonial

TESTIMONIALS = [
    {
        "quote": "TADIC giúp chúng tôi rút ngắn đáng kể thời gian khảo sát mặt đường và phát hiện hư hỏng sớm hơn nhiều so với phương pháp thủ công.",
        "author_name": "Ông Nguyễn Văn A",
        "author_title": "Trưởng phòng Quản lý hạ tầng",
        "order": 1,
    },
    {
        "quote": "Dashboard trực quan và báo cáo tự động của AI Inspection Platform giúp đội ngũ chúng tôi ra quyết định bảo trì nhanh và chính xác hơn.",
        "author_name": "Bà Trần Thị B",
        "author_title": "Giám đốc điều hành, Ban QLDA",
        "order": 2,
    },
    {
        "quote": "Hệ thống ATS Camera hoạt động ổn định 24/7, hỗ trợ cảnh báo sự cố kịp thời trên toàn tuyến quản lý của chúng tôi.",
        "author_name": "Ông Lê Văn C",
        "author_title": "Kỹ sư trưởng vận hành",
        "order": 3,
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample testimonials"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in TESTIMONIALS:
            author_name = data["author_name"]
            obj, was_created = Testimonial.objects.update_or_create(
                author_name=author_name,
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))
