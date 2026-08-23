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
