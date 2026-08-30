import re

from unidecode import unidecode

BXD_PATTERN = re.compile(r"-(BXD|BGTVT)\b", re.IGNORECASE)

TU_KHOA_TADIC = [
    "duong bo", "bao tri", "quan ly tai san ha tang", "dinh muc",
    "khao sat", "mat duong", "cau", "tcvn", "quy chuan",
    "chuyen doi so ha tang",
]


def la_van_ban_bxd(so_hieu: str) -> bool:
    """Trả về True nếu văn bản thuộc hệ thống Bộ Xây dựng
    (bao gồm cả văn bản GTVT cũ trước sáp nhập)."""
    return bool(BXD_PATTERN.search(so_hieu or ""))


def khop_tu_khoa(text: str) -> bool:
    t = unidecode((text or "").lower())
    return any(kw in t for kw in TU_KHOA_TADIC)


# Thứ tự trong danh sách này CHÍNH LÀ thứ tự ưu tiên: nếu văn bản khớp
# từ khoá của nhiều nhóm, nhóm nào đứng trước trong danh sách sẽ được
# chọn làm nhom_nghiep_vu chính.
NHOM_NGHIEP_VU = [
    ("duong_bo_cau",         "Đường bộ & Cầu",                       ["duong bo", "mat duong", "cau"]),
    ("bao_tri_tai_san",      "Bảo trì & Quản lý tài sản",            ["bao tri", "quan ly tai san ha tang"]),
    ("dinh_muc_khao_sat",    "Định mức & Khảo sát",                  ["dinh muc", "khao sat"]),
    ("tieu_chuan_quy_chuan", "Tiêu chuẩn – Quy chuẩn (TCVN/QCVN)",   ["tcvn", "quy chuan"]),
    ("chuyen_doi_so",        "Chuyển đổi số hạ tầng",                ["chuyen doi so ha tang"]),
]
NHOM_KHAC_ID, NHOM_KHAC_LABEL = "khac", "Khác"

# Thứ tự hiển thị các section trên trang /van-ban-phap-ly.
# "khac" luôn để cuối cùng.
THU_TU_HIEN_THI_NHOM = [nhom_id for nhom_id, _, _ in NHOM_NGHIEP_VU] + [NHOM_KHAC_ID]


def phan_nhom(text: str):
    """Xác định nhóm nghiệp vụ chính của văn bản dựa trên trich_yeu/linh_vuc.

    Trả về (nhom_nghiep_vu_id, nhom_nghiep_vu_label), hoặc None nếu văn bản
    không khớp bất kỳ từ khoá TADIC nào (không thuộc diện phân nhóm hiển thị).
    """
    t = unidecode((text or "").lower())
    for nhom_id, nhom_label, tu_khoa in NHOM_NGHIEP_VU:
        if any(kw in t for kw in tu_khoa):
            return nhom_id, nhom_label
    if khop_tu_khoa(text):  # khớp TU_KHOA_TADIC nói chung nhưng không rơi vào nhóm cụ thể
        return NHOM_KHAC_ID, NHOM_KHAC_LABEL
    return None
