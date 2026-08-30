from django.core.management.base import BaseCommand

from legalvb import notify_email, notify_zalo
from legalvb.fetch_rss import fetch_rss
from legalvb.fetch_vbpl_api import fetch_vbpl
from legalvb.filters import khop_tu_khoa, la_van_ban_bxd, phan_nhom
from legalvb.models import VanBanPhapLuat
from legalvb.normalize import map_trang_thai


class Command(BaseCommand):
    help = 'Đồng bộ văn bản pháp luật từ RSS Bộ Xây dựng + API ws.vbpl.vn'

    def handle(self, *args, **options):
        is_first_run = not VanBanPhapLuat.objects.exists()

        raw_records = fetch_rss() + fetch_vbpl()
        self.stdout.write(f'Fetch: {len(raw_records)} bản ghi thô')

        # dedupe trong batch theo (so_hieu, ngay_ban_hanh)
        seen = set()
        deduped = []
        for r in raw_records:
            key = (r['so_hieu'], r['ngay_ban_hanh'])
            if not r['so_hieu'] or key in seen:
                continue
            seen.add(key)
            deduped.append(r)

        skipped_not_bxd = 0
        created_records = []

        for r in deduped:
            if not la_van_ban_bxd(r['so_hieu']):
                skipped_not_bxd += 1
                continue

            uu_tien = khop_tu_khoa(r['trich_yeu'])
            nhom = phan_nhom(f"{r['trich_yeu']} {r['linh_vuc']}")
            nhom_nghiep_vu_id, nhom_nghiep_vu_label = nhom if nhom else (None, None)
            obj, created = VanBanPhapLuat.objects.update_or_create(
                so_hieu=r['so_hieu'],
                ngay_ban_hanh=r['ngay_ban_hanh'],
                defaults={
                    'loai_vb': r['loai_vb'],
                    'co_quan_ban_hanh': r['co_quan_ban_hanh'],
                    'ngay_hieu_luc': r['ngay_hieu_luc'],
                    'trich_yeu': r['trich_yeu'],
                    'linh_vuc': r['linh_vuc'],
                    'trang_thai_hieu_luc': map_trang_thai(r.get('trang_thai_raw', '')),
                    'url_goc': r['url_goc'],
                    'url_file': r['url_file'],
                    'nguon': r['nguon'],
                    'uu_tien': uu_tien,
                    'nhom_nghiep_vu_id': nhom_nghiep_vu_id,
                    'nhom_nghiep_vu_label': nhom_nghiep_vu_label,
                },
            )
            if created:
                created_records.append(obj)

        alert_records = [r for r in created_records if r.uu_tien]
        if not is_first_run and alert_records:
            notify_email.send_alert(alert_records)
            notify_zalo.send_alert(alert_records)
            VanBanPhapLuat.objects.filter(pk__in=[r.pk for r in alert_records]).update(da_canh_bao=True)
        elif is_first_run:
            self.stdout.write('Lần chạy đầu tiên: chỉ ghi dữ liệu, không gửi cảnh báo.')

        self.stdout.write(self.style.SUCCESS(
            f'Xong. Tổng {len(deduped)} sau dedupe, bỏ qua {skipped_not_bxd} (không thuộc BXD/BGTVT), '
            f'{len(created_records)} bản ghi mới, {len(alert_records)} cảnh báo.'
        ))
