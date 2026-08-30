from datetime import date
from types import SimpleNamespace

from django.test import TestCase

from .filters import khop_tu_khoa, la_van_ban_bxd, phan_nhom
from .models import VanBanPhapLuat
from .normalize import extract_so_hieu, from_rss_entry, map_trang_thai


class FiltersTest(TestCase):
    def test_la_van_ban_bxd_bxd(self):
        self.assertTrue(la_van_ban_bxd('10/2024/TT-BXD'))

    def test_la_van_ban_bxd_bgtvt(self):
        self.assertTrue(la_van_ban_bxd('22/2019/TT-BGTVT'))

    def test_la_van_ban_bxd_khac(self):
        self.assertFalse(la_van_ban_bxd('05/2020/QĐ-TTg'))

    def test_khop_tu_khoa_duong_bo(self):
        self.assertTrue(khop_tu_khoa('Quy định về bảo trì đường bộ'))

    def test_khop_tu_khoa_khong_khop(self):
        self.assertFalse(khop_tu_khoa('Quy định về thuế thu nhập cá nhân'))


class PhanNhomTest(TestCase):
    def test_uu_tien_nhom_dung_bo_khi_khop_nhieu_nhom(self):
        # Khớp cả duong_bo_cau lẫn bao_tri_tai_san -> chọn nhóm đứng trước.
        self.assertEqual(
            phan_nhom('Thông tư quy định về bảo trì đường bộ'),
            ('duong_bo_cau', 'Đường bộ & Cầu'),
        )

    def test_nhom_tieu_chuan_quy_chuan(self):
        self.assertEqual(
            phan_nhom('Quy chuẩn kỹ thuật quốc gia QCVN...'),
            ('tieu_chuan_quy_chuan', 'Tiêu chuẩn – Quy chuẩn (TCVN/QCVN)'),
        )

    def test_khong_khop_nhom_nao(self):
        self.assertIsNone(phan_nhom('Nghị định về đầu tư công'))


class NormalizeTest(TestCase):
    def test_extract_so_hieu(self):
        self.assertEqual(extract_so_hieu('Thông tư 10/2024/TT-BXD về ...'), '10/2024/TT-BXD')

    def test_extract_so_hieu_fallback(self):
        self.assertEqual(extract_so_hieu('Không có số hiệu rõ ràng'), 'Không có số hiệu rõ ràng')

    def test_map_trang_thai(self):
        self.assertEqual(map_trang_thai('Còn hiệu lực'), 'con_hieu_luc')
        self.assertEqual(map_trang_thai('gì đó lạ'), 'khong_ro')

    def test_from_rss_entry_so_hieu_trong_summary(self):
        # Tiêu đề RSS moc.gov.vn thường KHÔNG chứa số hiệu — số hiệu nằm
        # trong phần mô tả (summary), phải tìm ở đó.
        entry = SimpleNamespace(
            title='Thông tư ban hành Định mức kinh tế - kỹ thuật khảo sát đo sâu',
            summary='<p>Ngày 14/8/2026, Bộ Xây dựng có <a>Thông tư số 65/2026/TT-BXD</a> ban hành...</p>',
            link='http:moc.gov.vn/vn/Pages/chitiettin.aspx?IDNews=96328',
            published='8/15/2026 4:04:00 PM',
            published_parsed=None,
        )
        result = from_rss_entry(entry)
        self.assertEqual(result['so_hieu'], '65/2026/TT-BXD')
        self.assertEqual(result['ngay_ban_hanh'], date(2026, 8, 15))
        self.assertEqual(result['url_goc'], 'http://moc.gov.vn/vn/Pages/chitiettin.aspx?IDNews=96328')


class DedupeTest(TestCase):
    def test_update_or_create_khong_trung(self):
        defaults = dict(trich_yeu='Test', nguon='vbpl_api')
        VanBanPhapLuat.objects.update_or_create(
            so_hieu='10/2024/TT-BXD', ngay_ban_hanh=date(2024, 1, 1), defaults=defaults,
        )
        VanBanPhapLuat.objects.update_or_create(
            so_hieu='10/2024/TT-BXD', ngay_ban_hanh=date(2024, 1, 1), defaults=defaults,
        )
        self.assertEqual(VanBanPhapLuat.objects.count(), 1)
