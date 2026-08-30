from django.core.management.base import BaseCommand

from legalvb.filters import phan_nhom
from legalvb.models import VanBanPhapLuat


class Command(BaseCommand):
    help = (
        'Tính lại nhom_nghiep_vu_id/nhom_nghiep_vu_label cho các bản ghi đã có '
        'sẵn trong DB (dựa trên trich_yeu + linh_vuc). Chạy 1 lần sau khi thêm '
        'cột nhom_nghiep_vu_*, hoặc mỗi khi đổi danh sách NHOM_NGHIEP_VU.'
    )

    def handle(self, *args, **options):
        qs = VanBanPhapLuat.objects.all()
        updated = 0
        cleared = 0

        for vb in qs.iterator():
            nhom = phan_nhom(f'{vb.trich_yeu} {vb.linh_vuc}')
            nhom_id, nhom_label = nhom if nhom else (None, None)
            if vb.nhom_nghiep_vu_id != nhom_id or vb.nhom_nghiep_vu_label != nhom_label:
                vb.nhom_nghiep_vu_id = nhom_id
                vb.nhom_nghiep_vu_label = nhom_label
                vb.save(update_fields=['nhom_nghiep_vu_id', 'nhom_nghiep_vu_label'])
                updated += 1
                if nhom_id is None:
                    cleared += 1

        self.stdout.write(self.style.SUCCESS(
            f'Xong. {qs.count()} bản ghi kiểm tra, {updated} bản ghi được cập nhật nhóm '
            f'({cleared} trong số đó không khớp nhóm nào).'
        ))
