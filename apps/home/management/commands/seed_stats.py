from django.core.management.base import BaseCommand
from home.models import Stat

STATS = [
    {"label": "Km đường đã phân tích", "target_value": 1500, "suffix": "+", "icon": "fa-road", "order": 1},
    {"label": "Giảm công sức thủ công", "target_value": 60, "suffix": "%", "icon": "fa-clock", "order": 2},
    {"label": "Khảo sát đã xác thực", "target_value": 500, "suffix": "+", "icon": "fa-certificate", "order": 3},
    {"label": "Khách hàng & Đối tác", "target_value": 100, "suffix": "+", "icon": "fa-people-group", "order": 4},
]


class Command(BaseCommand):
    help = "Seed the database with sample stats"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in STATS:
            label = data["label"]
            obj, was_created = Stat.objects.update_or_create(
                label=label,
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))
