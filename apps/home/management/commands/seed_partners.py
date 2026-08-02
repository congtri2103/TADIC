from django.core.management.base import BaseCommand
from home.models import Partner

PARTNERS = [
    {"name": "Cục Đường bộ VN", "icon_class": "fa-building-columns", "order": 1},
    {"name": "Sở GTVT Hà Nội", "icon_class": "fa-city", "order": 2},
    {"name": "Sở GTVT TP.HCM", "icon_class": "fa-landmark", "order": 3},
    {"name": "Ban QLDA Đường bộ", "icon_class": "fa-bridge", "order": 4},
    {"name": "Tổng Cty XDCT", "icon_class": "fa-industry", "order": 5},
    {"name": "Đường sắt VN", "icon_class": "fa-train", "order": 6},
    {"name": "Tập đoàn CIENCO4", "icon_class": "fa-road", "order": 7},
    {"name": "Cienco 5", "icon_class": "fa-hard-hat", "order": 8},
    {"name": "VNPT", "icon_class": "fa-microchip", "order": 9},
    {"name": "Viettel IDC", "icon_class": "fa-cloud", "order": 10},
]


class Command(BaseCommand):
    help = "Seed the database with sample partners"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in PARTNERS:
            name = data["name"]
            obj, was_created = Partner.objects.update_or_create(
                name=name,
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))
