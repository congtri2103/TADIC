from django.core.management.base import BaseCommand
from home.models import Project

PROJECTS = [
    {
        "title": "Cao tốc Bắc - Nam",
        "description": "Khảo sát và phân tích mặt đường bằng AI trên toàn tuyến.",
        "image_url": "https://images.unsplash.com/photo-1508964942454-1a56651d54ac?w=800&q=60",
        "tags": "Cao tốc",
        "order": 1,
    },
    {
        "title": "Giao thông đô thị",
        "description": "Triển khai ATS Camera System giám sát giao thông thông minh.",
        "image_url": "https://images.unsplash.com/photo-1494412651409-8963ce7935a7?w=800&q=60",
        "tags": "Đô thị",
        "order": 2,
    },
    {
        "title": "Quốc lộ 1A",
        "description": "Lập báo cáo kiểm định tự động cho toàn tuyến quốc lộ.",
        "image_url": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&q=60",
        "tags": "Quốc lộ",
        "order": 3,
    },
    {
        "title": "Hệ thống cầu vượt",
        "description": "Giám sát kết cấu định kỳ bằng công nghệ AI.",
        "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=60",
        "tags": "Cầu vượt",
        "order": 4,
    },
    {
        "title": "Trung tâm điều hành",
        "description": "Dashboard quản lý tập trung dữ liệu toàn mạng lưới.",
        "image_url": "https://images.unsplash.com/photo-1473445730015-841f29a9490b?w=800&q=60",
        "tags": "Trung tâm",
        "order": 5,
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample projects"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in PROJECTS:
            title = data["title"]
            obj, was_created = Project.objects.update_or_create(
                title=title,
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))
