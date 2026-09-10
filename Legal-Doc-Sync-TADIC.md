# Legal Doc Sync – Tự động cập nhật văn bản pháp luật Bộ Xây dựng lên website TADIC

> Module tự động thu thập, chuẩn hoá, **phân nhóm nghiệp vụ** và đồng bộ các văn bản pháp luật (Thông tư, Nghị định, QCVN, TCVN...) do **Bộ Xây dựng (BXD)** ban hành, hiển thị dưới dạng mục "Văn bản liên quan" (gom theo nhóm) trên website công ty và (mở rộng) cấp dữ liệu cho **VRoad.AI** như một module cập nhật pháp lý tự động.

---

## 1. Bối cảnh & mục tiêu

**Vấn đề:** Team cần một trang "Văn bản liên quan" trên website công ty, liệt kê các văn bản mới ban hành liên quan đến đường bộ / hạ tầng giao thông / xây dựng, **gom theo từng nhóm nghiệp vụ** thay vì liệt kê phẳng một danh sách dài, luôn cập nhật mà không cần copy-paste thủ công từ `moc.gov.vn`.

**Ràng buộc quan trọng:**
- ❌ **Không crawl trực tiếp HTML của `moc.gov.vn`** — site chặn truy cập tự động theo `robots.txt`. Vi phạm điều khoản sử dụng và dễ bị block IP.
- ✅ Phải dùng các **kênh dữ liệu hợp lệ** (RSS / trang liệt kê chính thức / API có cấu trúc).
- ✅ Sau sự kiện **sáp nhập Bộ GTVT vào Bộ Xây dựng**, toàn bộ văn bản đường bộ (kể cả các Thông tư cũ ký hiệu `-BGTVT`) nay nằm trong hệ thống của BXD. Bộ lọc bắt buộc phải nhận diện **cả hai ký hiệu**: `-BXD` và `-BGTVT`.
- ✅ **(Mới)** Mỗi văn bản khớp từ khoá TADIC phải được gán vào **đúng 1 nhóm nghiệp vụ chính** để hiển thị theo section riêng trên trang web (xem mục 6.1).

**Mục tiêu đầu ra:**
1. Trang web công ty có mục văn bản pháp lý tự cập nhật, **gom theo nhóm nghiệp vụ** (không cần admin thao tác thủ công).
2. Dữ liệu có cấu trúc (không phải HTML thô) → có thể tái sử dụng làm module "cập nhật pháp lý tự động" gắn vào **VRoad.AI**, không chỉ dừng ở mục tin trên website.
3. Cảnh báo (Zalo/email) khi có văn bản mới thuộc nhóm từ khoá công ty theo dõi, **kèm tên nhóm nghiệp vụ** trong nội dung cảnh báo.

---

## 2. Nguồn dữ liệu (bắt buộc dùng đúng thứ tự ưu tiên)

Có 3 nguồn hợp lệ, xếp theo mức ưu tiên. **Tuyệt đối không crawl trực tiếp HTML của `moc.gov.vn`.**

| # | Nguồn | Địa chỉ | Đặc điểm | Ưu tiên |
|---|-------|---------|----------|---------|
| 1 | API CSDLQG về pháp luật | `ws.vbpl.vn` (cổng tra cứu: `vbpl.vn`) | Dữ liệu có cấu trúc, có trường **trạng thái hiệu lực** — nguồn **bền vững nhất**, nên dùng làm nguồn chính | ⭐⭐⭐ |
| 2 | RSS Cổng TTĐT Bộ Xây dựng | `moc.gov.vn/rss/1196/gioi-thieu-van-ban-moi.rss` ("Giới thiệu văn bản mới") | Có sẵn kênh RSS, dùng ngay, miễn phí — **đang là nguồn dữ liệu chính hoạt động tốt** (đã xác nhận qua thực tế triển khai) | ⭐⭐ |
| 3 | Trang Văn bản BXD | `moc.gov.vn/pl/pages/Vanban.aspx` | Bản gốc — chỉ dùng để **đối chiếu thủ công** và lấy `url_goc` / link file đính kèm, không dùng để crawl tự động hàng loạt | ⭐ (đối chiếu) |

**Chiến lược khuyến nghị:**
- Dùng **API `ws.vbpl.vn`** làm nguồn chính vì có trạng thái hiệu lực (còn hiệu lực / hết hiệu lực / sửa đổi) — tránh hiển thị văn bản đã hết hiệu lực trên site công ty.
  > ⚠️ **Cập nhật thực tế**: API `ws.vbpl.vn` hiện gọi được (không lỗi kết nối) nhưng trả về **0 kết quả** — nghi ngờ sai tham số/enum `TrangThaiBienTap`. Cần soi request thật qua DevTools trên `vbpl.vn` hoặc đăng ký tài khoản CSDLQG nếu API yêu cầu xác thực. **Việc này không chặn MVP** vì RSS đã đủ dùng làm nguồn chính tạm thời.
- Dùng **RSS BXD** (kênh "Giới thiệu văn bản mới") làm nguồn chính hiện tại — đã chạy tốt.
- Trang `Vanban.aspx` chỉ fetch **thủ công / tần suất thấp** khi cần đối chiếu số hiệu hoặc lấy link file gốc — không đưa vào cron job tần suất cao để tránh bị chặn.

> ⚠️ Nếu sau này cần dữ liệu từ `moc.gov.vn` mà RSS/API không có, phải liên hệ xin cấp quyền / API key chính thức, hoặc dùng dịch vụ scraping có sự đồng ý — không tự ý bypass `robots.txt`.

---

## 3. Kiến trúc tối thiểu (MVP)

```
Cron (n8n / GitHub Actions / systemd timer)
  → fetch RSS (moc.gov.vn) + API (ws.vbpl.vn)
  → chuẩn hoá schema
  → dedupe theo (so_hieu + ngay_ban_hanh)
  → lọc theo từ khoá TADIC + lọc ký hiệu -BXD / -BGTVT
  → phân nhóm nghiệp vụ (nhom_nghiep_vu_id / label) — MỚI, xem mục 6.1
  → ghi vào PostgreSQL
  → 1) render trang "Văn bản liên quan" theo từng nhóm nghiệp vụ (section riêng)
    2) cảnh báo Zalo/email khi có VB thuộc từ khoá theo dõi, kèm tên nhóm (tuỳ chọn, có thể để trống)
```

### 3.1 Lựa chọn đã áp dụng: tích hợp thành Django app

Đã quyết định (xem log trao đổi build): **tích hợp thành Django app mới** trong repo TADIC hiện có — `apps/legal_docs/` (hoặc tên tương đương), dùng ORM Django, management command `sync_vanban`, view render trang `/van-ban-lien-quan` dùng chung `base.html`/design system hiện có, **hiển thị nội dung gom theo nhóm nghiệp vụ** (xem mục 6.1 và 8). Đồng bộ tự động qua **systemd timer** trên VPS (`deploy/systemd/tadic-vanban-sync.service` + `.timer`, chạy mỗi 6h) — đã tạo file cấu hình, **chưa cài đặt vào server**, để dành cho lần deploy tiếp theo.

### 3.2 Luồng xử lý chi tiết

1. **Fetch**
   - Gọi RSS `moc.gov.vn/rss/1196/gioi-thieu-van-ban-moi.rss` → parse XML (dùng `feedparser` hoặc tương đương). ✅ Đang hoạt động.
   - Gọi API `ws.vbpl.vn` → parse JSON/XML trả về. ⏸️ Đang gỡ lỗi tham số (xem mục 2).
2. **Chuẩn hoá schema** — map dữ liệu thô của cả 2 nguồn về cùng 1 schema thống nhất (xem mục 4).
3. **Dedupe** — khoá trùng lặp là cặp `(so_hieu, ngay_ban_hanh)`, vì cùng 1 văn bản có thể xuất hiện ở cả RSS lẫn API.
4. **Lọc**
   - Lọc loại văn bản còn hiệu lực (`trang_thai_hieu_luc != "Hết hiệu lực"` — tuỳ nghiệp vụ có thể vẫn hiển thị văn bản hết hiệu lực nhưng gắn nhãn rõ).
   - Lọc theo **ký hiệu**: chấp nhận cả 2 pattern `-BXD` và `-BGTVT` (xem mục 5).
   - Lọc theo **từ khoá lĩnh vực** liên quan đến mảng nghiệp vụ TADIC (xem mục 6).
5. **Phân nhóm nghiệp vụ (MỚI)** — với văn bản khớp từ khoá TADIC, xác định **1 nhóm nghiệp vụ chính** (`nhom_nghiep_vu_id`, `nhom_nghiep_vu_label`) theo thứ tự ưu tiên đã định nghĩa (xem mục 6.1).
6. **Lưu trữ** — ghi vào PostgreSQL (bảng `van_ban_phap_luat`, giữ nguyên tên bảng/model kỹ thuật — xem lưu ý đổi tên ở mục 15), có `ngay_thu_thap` để biết lần crawl.
7. **Đầu ra**
   - Render lại trang "Văn bản liên quan" trên website — **hiển thị theo từng nhóm nghiệp vụ, mỗi nhóm 1 section riêng** (view Django đọc trực tiếp từ DB qua ORM, group theo `nhom_nghiep_vu_id`).
   - Gửi cảnh báo qua Zalo OA / email nếu văn bản mới khớp từ khoá theo dõi — nội dung cảnh báo kèm **tên nhóm nghiệp vụ** — **tuỳ chọn (optional)**, tự động skip nếu thiếu `ZALO_OA_ACCESS_TOKEN` / `LEGAL_ALERT_EMAIL_TO`, không gây lỗi hệ thống.

---

## 4. Schema dữ liệu chuẩn hoá

Bảng `van_ban_phap_luat`:

| Trường | Kiểu | Mô tả |
|---|---|---|
| `so_hieu` | text (unique cùng `ngay_ban_hanh`) | Số hiệu văn bản, ví dụ `10/2024/TT-BXD` |
| `loai_vb` | text | Loại văn bản: Thông tư, Nghị định, QCVN, TCVN, Quyết định... |
| `co_quan_ban_hanh` | text | Cơ quan ban hành (Bộ Xây dựng, Chính phủ...) |
| `ngay_ban_hanh` | date | Ngày ký ban hành |
| `ngay_hieu_luc` | date, nullable | Ngày có hiệu lực |
| `trich_yeu` | text | Trích yếu / tên đầy đủ văn bản |
| `linh_vuc` | text | Lĩnh vực (đường bộ, xây dựng, hạ tầng kỹ thuật...) — dữ liệu thô lấy từ nguồn |
| `trang_thai_hieu_luc` | text (enum) | `Còn hiệu lực` / `Hết hiệu lực` / `Sửa đổi bổ sung` / `Chưa có hiệu lực` |
| `uu_tien` | boolean | `True` nếu khớp ít nhất 1 từ khoá TADIC (mục 6) |
| `nhom_nghiep_vu_id` | text, nullable | **MỚI.** Mã nhóm nghiệp vụ dùng để group/filter trên UI, ví dụ `duong_bo_cau`. `NULL` nếu văn bản không khớp từ khoá TADIC nào (không thuộc diện ưu tiên hiển thị theo nhóm) — xem mục 6.1 |
| `nhom_nghiep_vu_label` | text, nullable | **MỚI.** Tên hiển thị tiếng Việt của nhóm (dùng thẳng lên UI), ví dụ `Đường bộ & Cầu` |
| `url_goc` | text | Link tới trang chi tiết văn bản (vbpl.vn hoặc moc.gov.vn) |
| `url_file` | text, nullable | Link file đính kèm (PDF/DOC) nếu có |
| `ngay_thu_thap` | timestamp | Thời điểm hệ thống ghi nhận bản ghi này |

```sql
CREATE TABLE van_ban_phap_luat (
    id                    BIGSERIAL PRIMARY KEY,
    so_hieu               TEXT NOT NULL,
    loai_vb               TEXT,
    co_quan_ban_hanh      TEXT,
    ngay_ban_hanh         DATE,
    ngay_hieu_luc         DATE,
    trich_yeu             TEXT,
    linh_vuc              TEXT,
    trang_thai_hieu_luc   TEXT,
    uu_tien               BOOLEAN NOT NULL DEFAULT FALSE,
    nhom_nghiep_vu_id      TEXT,
    nhom_nghiep_vu_label   TEXT,
    url_goc               TEXT,
    url_file              TEXT,
    ngay_thu_thap         TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (so_hieu, ngay_ban_hanh)
);

CREATE INDEX idx_vbpl_linh_vuc ON van_ban_phap_luat (linh_vuc);
CREATE INDEX idx_vbpl_ngay_ban_hanh ON van_ban_phap_luat (ngay_ban_hanh DESC);
CREATE INDEX idx_vbpl_nhom_nghiep_vu ON van_ban_phap_luat (nhom_nghiep_vu_id);
```

> **Migration cho dữ liệu cũ:** nếu bảng đã có dữ liệu từ trước (chưa có 2 cột `nhom_nghiep_vu_*`), sau khi chạy migration thêm cột, cần chạy 1 lần script backfill (`python manage.py backfill_nhom`) để tính lại nhóm cho các bản ghi cũ dựa trên `trich_yeu` + `linh_vuc` đã lưu — xem mục 11.

---

## 5. Bộ lọc ký hiệu văn bản (BXD / BGTVT)

**Bối cảnh:** Sau khi Bộ Giao thông Vận tải (GTVT) sáp nhập vào Bộ Xây dựng, toàn bộ văn bản lĩnh vực đường bộ — bao gồm cả các Thông tư ban hành **trước sáp nhập** với ký hiệu cũ `-BGTVT` — hiện đều thuộc hệ thống quản lý của Bộ Xây dựng.

➡️ **Bộ lọc số hiệu bắt buộc phải khớp cả hai hậu tố**, không được chỉ lọc `-BXD`:

```python
import re

BXD_PATTERN = re.compile(r"-(BXD|BGTVT)\b", re.IGNORECASE)

def la_van_ban_bxd(so_hieu: str) -> bool:
    """Trả về True nếu văn bản thuộc hệ thống Bộ Xây dựng
    (bao gồm cả văn bản GTVT cũ trước sáp nhập)."""
    return bool(BXD_PATTERN.search(so_hieu or ""))
```

> Viết test riêng cho hàm này với các case: `10/2024/TT-BXD`, `22/2019/TT-BGTVT`, `05/2020/QĐ-TTg` (phải False vì không thuộc BXD/BGTVT).

---

## 6. Bộ lọc theo từ khoá nghiệp vụ TADIC

Chỉ giữ lại (hoặc gắn nhãn ưu tiên cao) các văn bản có `trich_yeu` / `linh_vuc` khớp với nhóm từ khoá nghiệp vụ công ty:

```
đường bộ, bảo trì, quản lý tài sản hạ tầng, định mức,
khảo sát, mặt đường, cầu, TCVN, quy chuẩn, chuyển đổi số hạ tầng
```

Gợi ý cách lọc: chuẩn hoá chữ thường + bỏ dấu (dùng `unidecode`) trước khi so khớp substring, để tránh miss do khác biệt dấu câu tiếng Việt.

```python
from unidecode import unidecode

TU_KHOA_TADIC = [
    "duong bo", "bao tri", "quan ly tai san ha tang", "dinh muc",
    "khao sat", "mat duong", "cau", "tcvn", "quy chuan",
    "chuyen doi so ha tang",
]

def khop_tu_khoa(text: str) -> bool:
    t = unidecode((text or "").lower())
    return any(kw in t for kw in TU_KHOA_TADIC)
```

Văn bản khớp từ khoá → gắn cờ `uu_tien = True` → kích hoạt cảnh báo Zalo/email + được **phân nhóm nghiệp vụ** (mục 6.1) để hiển thị theo section riêng; văn bản không khớp vẫn có thể lưu vào DB nhưng không đẩy lên trang chủ / không cảnh báo / không thuộc nhóm nào (`nhom_nghiep_vu_id = NULL`) (tuỳ cấu hình `linh_vuc` mong muốn hiển thị công khai).

### 6.1 Phân nhóm nghiệp vụ (nhóm hiển thị) — MỚI

**Mục tiêu:** thay vì hiển thị tất cả văn bản khớp từ khoá thành 1 danh sách phẳng, gom chúng thành **các nhóm nghiệp vụ** để người dùng trên website dễ tìm theo chủ đề (ví dụ: chỉ xem văn bản về "Bảo trì & Quản lý tài sản" mà không phải lướt qua văn bản về "Tiêu chuẩn – Quy chuẩn").

**Nguyên tắc:**
- Nhóm được suy ra **trực tiếp từ bộ từ khoá TADIC** đã có ở mục 6 (không tạo taxonomy mới tách biệt, tránh phải bảo trì 2 danh sách từ khoá song song).
- **Giả định đã áp dụng (MVP): mỗi văn bản chỉ thuộc 1 nhóm chính** — nếu văn bản khớp từ khoá của nhiều nhóm cùng lúc, chọn nhóm có **thứ tự ưu tiên cao nhất** (duyệt từ trên xuống trong danh sách `NHOM_NGHIEP_VU`, nhóm nào khớp trước thì chọn nhóm đó). Việc này để đơn giản hoá UI/schema ở giai đoạn đầu; nếu sau này cần "1 văn bản – nhiều nhóm", xem gợi ý mở rộng ở cuối mục này.
- Văn bản khớp từ khoá TADIC nhưng không rơi vào 5 nhóm cụ thể bên dưới (trường hợp hiếm, do từ khoá tương lai được thêm mà chưa gán nhóm) → rơi vào nhóm dự phòng **"Khác"**.

**Bảng nhóm (5 nhóm chính + 1 nhóm dự phòng), xếp theo đúng thứ tự ưu tiên khi xét trùng:**

| # | `nhom_nghiep_vu_id` | Tên hiển thị (`nhom_nghiep_vu_label`) | Từ khoá TADIC thuộc nhóm |
|---|---|---|---|
| 1 | `duong_bo_cau` | Đường bộ & Cầu | `đường bộ`, `mặt đường`, `cầu` |
| 2 | `bao_tri_tai_san` | Bảo trì & Quản lý tài sản | `bảo trì`, `quản lý tài sản hạ tầng` |
| 3 | `dinh_muc_khao_sat` | Định mức & Khảo sát | `định mức`, `khảo sát` |
| 4 | `tieu_chuan_quy_chuan` | Tiêu chuẩn – Quy chuẩn (TCVN/QCVN) | `TCVN`, `quy chuẩn` |
| 5 | `chuyen_doi_so` | Chuyển đổi số hạ tầng | `chuyển đổi số hạ tầng` |
| — | `khac` | Khác | (khớp `khop_tu_khoa()` nhưng không rơi vào 5 nhóm trên) |

**Code (`apps/legal_docs/filters.py`, viết ngay cạnh `khop_tu_khoa()` đã có ở mục 6):**

```python
from unidecode import unidecode

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

# Thứ tự hiển thị các section trên trang /van-ban-lien-quan (mục 8).
# "khac" luôn để cuối cùng.
THU_TU_HIEN_THI_NHOM = [nhom_id for nhom_id, _, _ in NHOM_NGHIEP_VU] + [NHOM_KHAC_ID]


def phan_nhom(text: str) -> tuple[str, str] | None:
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
```

> Viết test cho `phan_nhom()` với các case:
> - `"Thông tư quy định về bảo trì đường bộ"` → khớp cả `duong_bo_cau` lẫn `bao_tri_tai_san`, kỳ vọng trả về `duong_bo_cau` (đứng trước trong danh sách ưu tiên).
> - `"Quy chuẩn kỹ thuật quốc gia QCVN..."` → `tieu_chuan_quy_chuan`.
> - `"Nghị định về đầu tư công"` (không khớp từ khoá nào) → `None`.

**Gợi ý mở rộng sau này (không làm ở MVP):** nếu cần "1 văn bản thuộc nhiều nhóm" thay vì chỉ 1 nhóm chính, tách bảng `van_ban_nhom` (many-to-many: `van_ban_id`, `nhom_nghiep_vu_id`) thay vì 2 cột phẳng trên `van_ban_phap_luat`. Không cần làm ngay vì tăng độ phức tạp UI (phải hiển thị 1 văn bản lặp lại ở nhiều section) mà lợi ích chưa rõ ở giai đoạn MVP.

---

## 7. Cảnh báo Zalo / Email (tuỳ chọn — optional)

Khi crawl phát hiện văn bản **mới** (chưa có trong DB) và **khớp từ khoá ưu tiên**:

- **Zalo OA**: gọi thẳng **Zalo OA API** (`openapi.zalo.me/v3.0/oa/message/cs`) bằng `ZALO_OA_ACCESS_TOKEN` + `ZALO_OA_RECIPIENT_ID`. Nếu có cấu hình thêm `ZALO_OA_WEBHOOK_URL` (ví dụ forward qua n8n), hàm sẽ **ưu tiên gửi qua webhook** thay vì gọi API trực tiếp.
- **Email**: gửi qua SMTP nội bộ hoặc dịch vụ (SendGrid/Mailgun) tới danh sách `LEGAL_ALERT_EMAIL_TO`.

**Cơ chế skip an toàn (đã xác nhận, đã sửa trong `notify_zalo.py`):**
- Nếu **`ZALO_OA_ACCESS_TOKEN` trống** → tự động bỏ qua bước gửi Zalo, không lỗi, không chặn pipeline.
- **Không còn bắt buộc** phải có `ZALO_OA_WEBHOOK_URL` — chỉ cần token là đủ để gọi API trực tiếp.
- Tương tự, nếu `LEGAL_ALERT_EMAIL_TO` trống → bỏ qua gửi email.

Nội dung cảnh báo tối thiểu: `so_hieu`, `trich_yeu`, **`nhom_nghiep_vu_label`** (MỚI — để người nhận biết ngay văn bản thuộc mảng nào), `ngay_ban_hanh`, `ngay_hieu_luc`, `url_goc`.

---

## 8. Hiển thị trên website công ty

- Trang **`/van-ban-lien-quan`** (đổi từ `/van-ban-phap-luat` — xem lý do đổi tên ở mục 15), dùng chung `base.html`/design system hiện có của website TADIC, view Django đọc trực tiếp từ PostgreSQL qua ORM.
- **(MỚI) Bố cục gom theo nhóm nghiệp vụ**, thay vì 1 danh sách phẳng:
  - View group các văn bản (`uu_tien = True`, có `nhom_nghiep_vu_id`) theo `nhom_nghiep_vu_id`, dùng thứ tự hiển thị cố định `THU_TU_HIEN_THI_NHOM` (mục 6.1) — không sort theo alphabet để tránh nhóm "Khác" nhảy lên đầu.
  - Trong mỗi nhóm, sort văn bản theo `ngay_ban_hanh DESC` (mới nhất trước).
  - Mỗi nhóm hiển thị dạng **section riêng, cuộn dọc** (đơn giản, đồng bộ với hiệu ứng so le trắng/xanh dương ở mục 14): tiêu đề nhóm (`nhom_nghiep_vu_label`) + số lượng văn bản trong nhóm, bên dưới là danh sách/thẻ văn bản của nhóm đó.
  - Nhóm **"Khác"** đặt cuối cùng, có thể để dạng thu gọn (collapsed) mặc định nếu số lượng nhiều, tránh chiếm quá nhiều chỗ trên trang.
  - Văn bản không khớp từ khoá nào (`nhom_nghiep_vu_id IS NULL`) **không hiển thị** trên trang này (giữ nguyên hành vi cũ ở mục 6), chỉ lưu trong DB để dự phòng/đối chiếu sau.
- Mỗi văn bản trong section hiển thị: số hiệu, loại VB, trích yếu, ngày ban hành, trạng thái hiệu lực (badge màu), link file/link gốc.
- Có thể thêm bộ lọc phía client theo `trang_thai_hieu_luc` (còn hiệu lực / hết hiệu lực) áp dụng trong phạm vi từng nhóm — không bắt buộc ở đợt này.
- **Thêm mục "Văn bản liên quan" vào thanh điều hướng chính (navbar)** — xem chi tiết mục 15.

**Ví dụ cấu trúc HTML mẫu (`templates/legal_docs/van_ban_phap_ly.html`):**

```html
{% for nhom in nhom_list %}
<section class="vbpl-nhom" id="nhom-{{ nhom.id }}">
  <h2>{{ nhom.label }} <span class="vbpl-nhom__count">({{ nhom.van_ban_list|length }})</span></h2>
  <div class="vbpl-danh-sach">
    {% for vb in nhom.van_ban_list %}
      <article class="vbpl-item">
        <span class="vbpl-item__so-hieu">{{ vb.so_hieu }}</span>
        <span class="vbpl-item__trich-yeu">{{ vb.trich_yeu }}</span>
        <span class="vbpl-item__ngay">{{ vb.ngay_ban_hanh }}</span>
        <span class="vbpl-item__badge vbpl-item__badge--{{ vb.trang_thai_hieu_luc|slugify }}">
          {{ vb.trang_thai_hieu_luc }}
        </span>
        <a href="{{ vb.url_goc }}" target="_blank" rel="noopener">Xem văn bản gốc</a>
      </article>
    {% endfor %}
  </div>
</section>
{% endfor %}
```

**View (`apps/legal_docs/views.py`) — gợi ý cách group trong Python (không cần thêm thư viện):**

```python
from itertools import groupby
from .filters import THU_TU_HIEN_THI_NHOM, NHOM_NGHIEP_VU, NHOM_KHAC_ID, NHOM_KHAC_LABEL

NHOM_LABEL_MAP = {nhom_id: label for nhom_id, label, _ in NHOM_NGHIEP_VU}
NHOM_LABEL_MAP[NHOM_KHAC_ID] = NHOM_KHAC_LABEL

def van_ban_phap_ly_view(request):
    van_ban_qs = (
        VanBanPhapLuat.objects
        .filter(uu_tien=True, nhom_nghiep_vu_id__isnull=False)
        .order_by("ngay_ban_hanh")  # sort tăng dần để groupby hoạt động đúng, sort giảm dần lại trong Python bên dưới
    )
    theo_nhom = {}
    for vb in van_ban_qs:
        theo_nhom.setdefault(vb.nhom_nghiep_vu_id, []).append(vb)

    nhom_list = []
    for nhom_id in THU_TU_HIEN_THI_NHOM:
        van_ban_list = sorted(
            theo_nhom.get(nhom_id, []), key=lambda vb: vb.ngay_ban_hanh, reverse=True
        )
        if van_ban_list:  # không hiển thị section rỗng
            nhom_list.append({
                "id": nhom_id,
                "label": NHOM_LABEL_MAP[nhom_id],
                "van_ban_list": van_ban_list,
            })

    return render(request, "legal_docs/van_ban_phap_ly.html", {"nhom_list": nhom_list})
```

---

## 9. Mở rộng: module cho VRoad.AI

Giá trị cộng thêm quan trọng nhất của hệ thống này: đây không chỉ là "mục tin tức" trên website, mà là **mảnh ghép "cập nhật pháp lý tự động"** có thể gắn thẳng vào **VRoad.AI** như một module nghiệp vụ — ví dụ: tự động đối chiếu quy chuẩn/định mức bảo trì đường bộ mới nhất khi VRoad.AI tính toán chỉ số IRI, phân cấp mức độ hư hỏng hoặc lập kế hoạch bảo trì.

Vì dữ liệu đã được chuẩn hoá schema (mục 4, bao gồm cả `nhom_nghiep_vu_id`) và lưu trong PostgreSQL, việc tích hợp chỉ cần expose thêm 1 API nội bộ (`GET /api/vanban?nhom=duong_bo_cau&trang_thai=...`) để VRoad.AI gọi tới theo đúng nhóm nghiệp vụ cần — không cần xây lại pipeline crawl riêng.

---

## 10. Việc cần làm (đề xuất lộ trình build bằng Claude)

- [x] **Bước 1 — Khảo sát API `ws.vbpl.vn`**: endpoint gọi được, nhưng tham số `TrangThaiBienTap` sai/thiếu enum đúng → trả 0 kết quả. **Cần tiếp tục**: soi request thật qua DevTools trên `vbpl.vn`, hoặc đăng ký tài khoản CSDLQG nếu cần xác thực.
- [x] **Bước 2 — Viết parser RSS** cho kênh "Giới thiệu văn bản mới" — ✅ hoạt động tốt, đang là nguồn chính.
- [ ] **Bước 3 — Viết parser API** cho `ws.vbpl.vn` — chờ xử lý xong Bước 1.
- [x] **Bước 4 — Viết hàm dedupe + lọc** (`la_van_ban_bxd`, `khop_tu_khoa`) kèm unit test.
- [x] **Bước 5 — Thiết lập PostgreSQL** theo schema mục 4, viết migration (qua Django ORM/migrations).
- [x] **Bước 6 — Viết job tổng hợp** (`sync_vanban` management command).
- [x] **Bước 7 — Thiết lập lịch chạy tự động**: đã tạo `deploy/systemd/tadic-vanban-sync.service` + `.timer` (chạy mỗi 6h) — **chưa cài vào VPS**, để dành đợt deploy tới.
- [x] **Bước 8 — Cảnh báo Zalo/email** — đã code xong, hoạt động optional/skip an toàn khi thiếu credentials thật.
- [x] **Bước 9 — Trang hiển thị** `/van-ban-lien-quan` — route + label đã đổi theo mục 15 (app thực tế đặt tên `legalvb`, mount tại `van-ban-lien-quan/` trong `config/urls.py`), dùng chung `home/base.html`.
- [x] **Bước 9b — (MỚI) Phân nhóm nghiệp vụ**: đã thêm cột `nhom_nghiep_vu_id` / `nhom_nghiep_vu_label` (migration `0002_...`), viết hàm `phan_nhom()` trong `filters.py`, gọi trong `sync_vanban.py` ngay sau bước lọc từ khoá (mục 6.1), có unit test `PhanNhomTest` trong `tests.py`.
- [x] **Bước 9c — (MỚI) Backfill dữ liệu cũ**: đã viết `management/commands/backfill_nhom.py`, đã chạy trên DB dev — 7/17 bản ghi cũ được gán nhóm.
- [x] **Bước 9d — (MỚI) Cập nhật view + template hiển thị theo nhóm**: `views.py` group văn bản theo `nhom_nghiep_vu_id` (mục 8), template `van_ban_list.html` render từng `<section class="vbpl-nhom">` theo nhóm (dùng partial `_van_ban_cards.html`), CSS `.vbpl-nhom__*` thêm vào `static/css/style.css`.
- [x] **Bước 9e — (MỚI) Cập nhật nội dung cảnh báo Zalo/email**: đã thêm `nhom_nghiep_vu_label` vào nội dung cảnh báo trong `notify_zalo.py` và `notify_email.py` — xem mục 7.
- [x] **Bước 10 — (Mở rộng)** `van_ban_api` (`GET /van-ban-lien-quan/api/`) hỗ trợ filter theo `?nhom=<id>`, trả kèm `nhom_nghiep_vu_id`/`nhom_nghiep_vu_label` — sẵn sàng cho VRoad.AI gọi (mục 9).
- [x] **Bước 11 — (Mới) Giao diện màu so le trắng/xanh dương**: trang chủ (`home/index.html`) đã dùng `section--light` / `section--dark` so le sẵn (theme "Base CRM", màu brand qua `--color-primary`, cập nhật thành `#2559D8` — xem mục 14). Trang `/van-ban-lien-quan` nay cũng áp so le `section--light`/`section--dark` cho từng section nhóm nghiệp vụ (mục 8), nhóm "Khác" thu gọn mặc định bằng `<details>`.
- [x] **Bước 12 — (Mới) Đổi tên hiển thị** "Văn bản pháp luật" → "Văn bản liên quan": đã có sẵn trên UI (`<title>`, `<h1>`, breadcrumb) và trong navbar chính (`home/base.html`, giữa "Tin tức" và "Liên hệ") — xem mục 15.
- [x] **Bước 13 — (MỚI) Cập nhật màu brand `--color-primary`**: đổi giá trị hex sang `#2559D8` (thay cho tông màu cũ trước đó dùng trên site), áp dụng cho toàn bộ nơi đang tham chiếu biến này (nút CTA, badge, section--dark, navbar active-state...) — xem mục 14.4.

---

## 11. Cấu trúc thư mục thực tế (đã tích hợp vào repo TADIC)

```
TADIC/                                # Repo Django hiện có của công ty
├── apps/
│   ├── home/
│   └── legal_docs/                   # App mới cho module này
│       ├── management/
│       │   └── commands/
│       │       ├── sync_vanban.py    # Entry point: fetch → chuẩn hoá → dedupe → lọc → PHÂN NHÓM → lưu DB
│       │       └── backfill_nhom.py  # MỚI: tính lại nhom_nghiep_vu_* cho dữ liệu cũ, chạy 1 lần sau migration
│       ├── models.py                 # Model VanBanPhapLuat (map schema mục 4, gồm nhom_nghiep_vu_id/label)
│       ├── views.py                  # View render trang /van-ban-lien-quan (group theo nhóm — mục 8)
│       ├── fetch_rss.py
│       ├── fetch_vbpl_api.py
│       ├── normalize.py
│       ├── filters.py                # la_van_ban_bxd(), khop_tu_khoa(), phan_nhom(), NHOM_NGHIEP_VU (MỚI — mục 6.1)
│       ├── dedupe.py
│       ├── notify_zalo.py
│       ├── notify_email.py
│       └── migrations/
│           └── ...
│           # migration MỚI cần thêm: add_field nhom_nghiep_vu_id, nhom_nghiep_vu_label + index
├── templates/
│   └── legal_docs/
│       └── van_ban_phap_ly.html      # Dùng chung base.html hiện có, render section theo từng nhóm (mục 8)
├── deploy/
│   └── systemd/
│       ├── tadic-vanban-sync.service
│       └── tadic-vanban-sync.timer
├── tests/
│   ├── test_filters.py               # gồm cả test cho phan_nhom() — MỚI
│   ├── test_normalize.py
│   └── test_dedupe.py
└── .env                              # Xem mục 12
```

---

## 12. Biến môi trường (thực tế đang dùng)

```
# Django
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=
DJANGO_ALLOWED_HOSTS=tadic.vn,www.tadic.vn,SERVER_IP
DJANGO_CSRF_TRUSTED_ORIGINS=https://tadic.vn,https://www.tadic.vn

# PostgreSQL
DATABASE_URL=postgresql://user:password@127.0.0.1:5432/tadic_db

# Legal Doc Sync — Văn bản liên quan
VBPL_API_BASE=https://ws.vbpl.vn
MOC_RSS_URL=http://moc.gov.vn/rss/1196/gioi-thieu-van-ban-moi.rss

# Cảnh báo (tuỳ chọn — để trống nếu chưa có, hệ thống tự skip)
LEGAL_ALERT_EMAIL_TO=
ZALO_OA_ACCESS_TOKEN=
ZALO_OA_WEBHOOK_URL=
ZALO_OA_RECIPIENT_ID=

# Cron ngoài (nếu dùng GitHub Actions gọi API sync thay vì systemd timer)
SYNC_API_TOKEN=
```

> Không cần thêm biến môi trường mới cho việc phân nhóm — danh sách nhóm (`NHOM_NGHIEP_VU`) là hằng số cố định trong code (`filters.py`), không cấu hình qua `.env`, vì đây là logic nghiệp vụ ổn định, không phải secret hay cấu hình theo môi trường. Màu brand (`--color-primary`, mục 14.4) cũng là hằng số CSS, không đưa vào `.env`.

---

## 13. Rủi ro & lưu ý khi triển khai

| Rủi ro | Giải pháp |
|---|---|
| API `ws.vbpl.vn` chưa xác định rõ contract (endpoint/tham số/auth), hiện trả 0 kết quả | Soi request thật qua DevTools trên `vbpl.vn` khi tra cứu thủ công; đăng ký tài khoản CSDLQG nếu cần xác thực. Không chặn MVP vì RSS đã đủ dùng |
| RSS đổi cấu trúc / đổi URL | Bọc `fetch_rss.py` bằng try/except, log lỗi, không để job chết toàn bộ pipeline |
| Trùng lặp văn bản do sai khác nhỏ ở số hiệu (khoảng trắng, hoa/thường) | Chuẩn hoá `so_hieu` (strip, upper-case phần ký hiệu) trước khi dùng làm khoá dedupe |
| Văn bản GTVT cũ bị bỏ sót do chỉ lọc `-BXD` | Đã xử lý ở mục 5 — luôn test cả 2 pattern `-BXD` và `-BGTVT` |
| **(MỚI)** Văn bản khớp từ khoá của nhiều nhóm cùng lúc, dễ gây tranh cãi "đáng lẽ phải ở nhóm khác" | Đã xử lý bằng thứ tự ưu tiên cố định trong `NHOM_NGHIEP_VU` (mục 6.1) — nếu nghiệp vụ thay đổi cách ưu tiên, chỉ cần đổi thứ tự trong danh sách, không cần sửa logic |
| **(MỚI)** Dữ liệu cũ trong DB (trước khi có `nhom_nghiep_vu_*`) sẽ không hiển thị ở trang mới vì `nhom_nghiep_vu_id IS NULL` | Bắt buộc chạy `backfill_nhom.py` (Bước 9c, mục 10) ngay sau khi deploy migration thêm cột, trước khi bật trang hiển thị theo nhóm |
| **(MỚI)** Thêm/bớt nhóm sau này làm lệch dữ liệu cũ (văn bản đã gán nhóm theo danh sách từ khoá cũ) | Coi `NHOM_NGHIEP_VU` là "danh sách có version" — mỗi lần đổi danh sách nhóm/từ khoá, chạy lại `backfill_nhom.py` để đồng bộ toàn bộ dữ liệu, không chỉ áp cho bản ghi mới |
| Cảnh báo spam khi lần đầu chạy job với DB rỗng | Thêm cờ "first run" — lần chạy đầu tiên chỉ ghi dữ liệu, không gửi cảnh báo hàng loạt |
| Vi phạm robots.txt nếu vô tình fallback sang crawl HTML | Không implement bất kỳ HTML scraper nào cho `moc.gov.vn`; nếu thiếu dữ liệu, ưu tiên bổ sung qua API/RSS hoặc liên hệ xin quyền truy cập chính thức |
| Zalo OA access token hết hạn (token ngắn hạn) | Cần xử lý refresh token nếu dùng lâu dài — kiểm tra `notify_zalo.py` đã hỗ trợ refresh chưa, nếu chưa thì thêm sau |
| **(MỚI)** Đổi route public (`/van-ban-phap-ly/` → `/van-ban-lien-quan/`, mục 15.1) làm gãy các nơi *khác* đang gọi thẳng URL cũ ngoài trang web (không tự chuyển hướng được vì không phải request GET của trình duyệt/không follow redirect) | Rà soát mọi chỗ hardcode URL cũ ngoài navbar: đã phát hiện và sửa `vercel.json` (`crons[0].path`) và `.github/workflows/sync-vanban.yml` (`SYNC_URL`) — 2 job cron gọi endpoint `cron/sync/` trực tiếp, nếu để trỏ URL cũ sẽ nhận redirect 301 thay vì response thật, dễ gây lỗi im lặng. Mỗi lần đổi route public sau này, luôn `grep -r` toàn repo (config CI/CD, `.env`, script deploy) trước khi merge |
| `.env` thật (`SERVER_IP`, SMTP, Zalo token...) bị commit nhầm vào Git | Đảm bảo `.env` nằm trong `.gitignore`, chỉ dùng `.env.example`/`.env.vps.example` làm mẫu công khai |
| **(MỚI)** Đổi màu brand (`--color-primary`) có thể ảnh hưởng nhiều nơi đang tham chiếu biến này (không riêng trang văn bản pháp lý) | Vì dùng biến CSS tập trung (không hard-code hex rải rác), chỉ cần sửa 1 chỗ khai báo trong `variables.css` (mục 14.4) là toàn site đổi theo — nhưng vẫn nên rà lại các chỗ có thể đã hard-code hex cũ ngoài biến (nếu có) để tránh lệch màu cục bộ |

---

## 14. Yêu cầu bổ sung — Giao diện: màu nền so le trắng/xanh dương

**Bối cảnh:** tham khảo phong cách landing page dạng "Base CRM" (ảnh minh hoạ đính kèm trong trao đổi nội bộ) — các section trên trang được **so le nền trắng và nền xanh dương đậm (brand color)** liên tiếp nhau, tạo nhịp thị giác rõ ràng khi cuộn trang, thay vì toàn bộ nền trắng đơn điệu như hiện tại.

### 14.1 Nguyên tắc áp dụng

- Chia trang thành các **section khối lớn** theo chiều dọc (hero, giới thiệu, dịch vụ/giải pháp, dự án nổi bật, CTA liên hệ...).
- Áp màu nền **so le**: section 1 trắng → section 2 xanh dương đậm (brand) → section 3 trắng → section 4 xanh dương đậm... (không cố định thứ tự tuyệt đối, miễn xen kẽ, tránh 2 section cùng màu liền kề).
- Khi nền là xanh dương đậm: chữ chuyển sang **trắng/màu sáng** để đảm bảo tương phản (không giữ nguyên chữ đen trên nền xanh đậm).
- Không đổi màu tổng thể `body`/`header` cố định — chỉ đổi nền theo từng `<section>`, để header/navbar vẫn nhất quán khi cuộn qua nhiều section màu khác nhau (dùng nền trong suốt hoặc nền riêng cố định cho `<nav>`).

### 14.2 Cách làm kỹ thuật (CSS variables — tái sử dụng design system hiện có)

Không tạo màu mới tuỳ tiện — tái sử dụng biến màu thương hiệu đã khai báo sẵn trong `variables.css` của website (`--color-primary` hoặc tương đương).

```css
/* variables.css — bổ sung nếu chưa có */
:root {
  --section-bg-light: #FFFFFF;
  --section-bg-dark: var(--color-primary);      /* dùng lại xanh dương thương hiệu hiện có, KHÔNG hard-code hex mới ở đây */
  --section-text-on-dark: #FFFFFF;
  --section-text-on-light: var(--color-text, #1E1E1E);
}

.section--light {
  background-color: var(--section-bg-light);
  color: var(--section-text-on-light);
}

.section--dark {
  background-color: var(--section-bg-dark);
  color: var(--section-text-on-dark);
}

/* Đảm bảo các thành phần con (link, badge, border) trong section--dark
   cũng đổi biến thể màu tương phản, không giữ style mặc định của theme sáng */
.section--dark a { color: var(--section-text-on-dark); }
.section--dark .card { background-color: rgba(255, 255, 255, 0.06); }
```

```html
<!-- Cấu trúc HTML mẫu, áp dụng so le class trực tiếp trên từng <section> -->
<section class="section--dark hero">...</section>
<section class="section--light gioi-thieu">...</section>
<section class="section--dark giai-phap">...</section>
<section class="section--light du-an">...</section>
<section class="section--dark lien-he-cta">...</section>
```

### 14.3 Phạm vi áp dụng đợt này

- Áp dụng cho **trang chủ** trước (nơi hiệu ứng so le rõ tác dụng nhất về mặt trình bày).
- Trang **`/van-ban-lien-quan`** (module đang build): danh sách văn bản dùng nền trắng là chính (dễ đọc bảng dữ liệu dài), chỉ phần **hero/tiêu đề đầu trang** áp `section--dark` cho đồng bộ phong cách toàn site. **(Tuỳ chọn)** nếu muốn tạo nhịp thị giác giữa các nhóm nghiệp vụ ở mục 8, có thể áp `section--light` / `section--dark` so le cho từng `<section class="vbpl-nhom">` — không bắt buộc ở đợt build này, có thể để toàn bộ nền trắng trước rồi thử nghiệm sau.
- Không bắt buộc áp cho các trang nội dung dài khác (Tin tức, chi tiết dự án...) trong đợt này — có thể mở rộng sau nếu duyệt hiệu ứng ổn trên trang chủ.

### 14.4 Cập nhật màu brand (MỚI) — thay màu xanh lá bằng xanh dương `#2559D8`

**Bối cảnh:** màu brand hiện dùng cho `--color-primary` (nền `section--dark`, nút CTA, badge ưu tiên, trạng thái active trên navbar...) đang là **xanh lá**. Team quyết định đổi sang **xanh dương**, lấy đúng theo mẫu màu đính kèm (ảnh dải màu đặc, đo được `RGB(37, 89, 216)` → **`#2559D8`**).

**Nguyên tắc đổi màu:**
- Vì toàn bộ hệ thống đã dùng biến CSS tập trung (`--color-primary`, xem mục 14.2), **chỉ cần sửa 1 dòng khai báo** trong `variables.css` — không sửa rải rác từng file.
- Không tạo thêm biến mới song song (`--color-primary-new` chẳng hạn) — sửa trực tiếp giá trị của `--color-primary` để mọi nơi tham chiếu (section so le, nút "Liên hệ", badge `uu_tien`, trạng thái active navbar, hero trang `/van-ban-lien-quan`...) tự động đổi theo.
- Rà soát thêm các biến phái sinh nếu có (ví dụ `--color-primary-light`, `--color-primary-dark` dùng cho hover/focus state) để đảm bảo đồng bộ tông màu xanh dương mới, tránh lệch màu cục bộ giữa các state.

```css
/* variables.css */
:root {
  /* Trước: --color-primary: #<mã xanh lá cũ>; */
  --color-primary: #2559D8;   /* MỚI — xanh dương brand, theo mẫu màu đính kèm */

  /* Nếu đang có biến phái sinh, cân nhắc cập nhật đồng bộ, ví dụ: */
  /* --color-primary-hover: #1E47B0;  (tối hơn ~15% để làm hover state) */
}
```

> **Việc cần làm khi triển khai:** mở `variables.css` (hoặc file tương đương chứa `--color-primary`), tìm dòng khai báo hex xanh lá hiện tại, thay bằng `#2559D8`. Sau đó kiểm tra lại toàn site (không chỉ trang chủ và `/van-ban-lien-quan`) ở các vị trí dùng `--color-primary` hoặc có thể đã hard-code hex xanh lá riêng lẻ ngoài biến (nút, icon, border, badge...) để đảm bảo không còn sót màu cũ.

---

## 15. Yêu cầu bổ sung — Đổi tên & thêm mục vào thanh điều hướng

### 15.1 Đổi tên hiển thị: "Văn bản pháp luật" → "Văn bản pháp lý" → "Văn bản liên quan" (MỚI — tên cuối cùng)

> **Lịch sử đổi tên:** Ban đầu là "Văn bản pháp luật" (thuật ngữ hành chính chuẩn xác), sau đổi sang "Văn bản pháp lý" (gọi phổ thông, dễ đọc hơn), và **theo yêu cầu mới nhất của Chú Thuận (cấu trúc navbar mới), tên hiển thị cuối cùng chốt là "Văn bản liên quan"**. Đây là lựa chọn về mặt thương hiệu/UX của TADIC, không phải lỗi sai — chỉ áp dụng tên mới nhất, các tên cũ không còn dùng ở bất kỳ đâu trên UI.

**Phạm vi đổi tên (chỉ đổi phần hiển thị cho người dùng, KHÔNG đổi tên kỹ thuật nội bộ để tránh phá vỡ dữ liệu/migration đã có):**

| Vị trí | Ban đầu | Đổi lần 1 | Đổi lần 2 (chốt) |
|---|---|---|---|
| Label trên navbar | *(chưa có)* | Văn bản pháp lý | **Văn bản liên quan** |
| Tiêu đề trang (`<h1>`, `<title>`) | Văn bản pháp luật | Văn bản pháp lý | **Văn bản liên quan** |
| URL / route | `/van-ban-phap-luat` | `/van-ban-phap-ly` | **`/van-ban-lien-quan`** |
| Breadcrumb, meta description | Văn bản pháp luật | Văn bản pháp lý | **Văn bản liên quan** |

> Nếu route `/van-ban-phap-ly` đã từng lên production trước khi đổi lần này, cần thêm `redirect 301` từ cả `/van-ban-phap-luat` lẫn `/van-ban-phap-ly` sang `/van-ban-lien-quan`.

**Giữ nguyên (không đổi), vì là tên kỹ thuật nội bộ, đổi sẽ tốn công migrate không cần thiết:**
- Tên bảng DB: `van_ban_phap_luat`
- Tên app Django: `legal_docs`
- Tên model: `VanBanPhapLuat`
- Tên biến môi trường: `LEGAL_ALERT_EMAIL_TO`, `MOC_RSS_URL`...
- Tên trường mới `nhom_nghiep_vu_id` / `nhom_nghiep_vu_label` (mục 6.1) — dùng tiếng Việt không dấu theo đúng convention đặt tên đã có của các trường khác trong bảng (`so_hieu`, `trich_yeu`...).

> Nếu route cũ `/van-ban-phap-luat` đã từng được chia sẻ/index bởi Google trước đó, cân nhắc thêm `redirect 301` từ route cũ sang route mới để không mất SEO — việc này chỉ cần thiết nếu trang đã lên production trước khi đổi tên.

### 15.2 Thêm mục vào thanh điều hướng chính (navbar)

**(CẬP NHẬT — theo yêu cầu mới nhất của Chú Thuận, thay thế toàn bộ cấu trúc navbar cũ bên dưới):**

Navbar cũ (đã lỗi thời):

```
Trang chủ · Về chúng tôi · Giải pháp ▾ · Sản phẩm ▾ · Dự án · Tin tức · [Liên hệ →]
```

➡️ **Navbar mới**, thay thế hoàn toàn cấu trúc trên — **bỏ mục "Sản phẩm"**, đổi/gộp các mục còn lại:

```
Giới thiệu · Giải pháp ứng dụng AI ▾ · Video · Tin tức & sự kiện · Văn bản liên quan · [Liên hệ →]
```

> ✅ **Đã triển khai (2026-08-30)** trong `apps/home/templates/home/base.html` — xem cột "Trạng thái thực tế" bên dưới. **2 điểm sai khác tạm thời** so với đặc tả gốc (dropdown giữ 11 mục động thay vì 7 mục tĩnh; "Video" chưa thêm) là **quyết định tạm thời của NC khi build**, không phải xác nhận chính thức từ Chú Thuận — cần chốt lại trước khi lên production, xem ghi chú "còn treo" bên dưới bảng.

| # | Mục navbar | Ghi chú thay đổi | Trạng thái thực tế |
|---|---|---|---|
| 1 | **Giới thiệu** | Gộp/thay cho "Trang chủ" + "Về chúng tôi" cũ | ✅ Đã đổi, trỏ tạm về `/ve-tadic/` (route "Về chúng tôi" cũ) — **còn treo:** chưa xác nhận với Chú Thuận đây có phải đích đến đúng ý hay cần 1 trang "Giới thiệu" riêng mới |
| 2 | **Giải pháp ứng dụng AI** ▾ | Đổi tên từ "Giải pháp", có dropdown 7 mục con (xem bảng bên dưới) | ⚠️ Label đã đổi, nhưng dropdown **giữ nguyên 11 mục động lấy từ DB** (model `Product`), **không** thay bằng 7 mục tĩnh — quyết định tạm để không mất dữ liệu/link chi tiết đã có. **Còn treo:** cần Chú Thuận xác nhận danh sách 7 mục có phải nghiệp vụ thật cần map lại 11 mục hiện có, hay chỉ là ảnh minh hoạ |
| 3 | **Video** | Mục mới, chưa có trước đây | ❌ **Chưa thêm vào navbar** — chưa có trang đích/nội dung, tạm bỏ qua ở đợt build này để tránh link chết. Còn treo, chờ xác nhận |
| 4 | **Tin tức & sự kiện** | Đổi tên từ "Tin tức" | ✅ Đã đổi (label only, chưa mở rộng loại nội dung "sự kiện" trong model bài viết) |
| 5 | **Văn bản liên quan** | Đổi tên từ "Văn bản pháp lý" (xem mục 15.1) — route đổi thành `/van-ban-lien-quan` | ✅ Đã đổi label + route; redirect 301 từ `/van-ban-phap-ly/` đã thêm trong `config/urls.py` |
| — | ~~Sản phẩm~~ | **Bỏ hẳn khỏi navbar** theo yêu cầu — không còn dropdown "Sản phẩm" | ✅ Đã xoá hẳn markup dropdown khỏi `base.html` (không chỉ ẩn CSS). Trang `/san-pham/` và link trong footer vẫn giữ nguyên, không bị ảnh hưởng |
| — | ~~Dự án~~ | Không còn xuất hiện trong menu mới — cần xác nhận lại với Chú Thuận xem có gộp vào "Giới thiệu" hay bỏ hẳn, vì menu gửi qua ảnh không nhắc tới mục này | ✅ Đã bỏ khỏi navbar chính theo quyết định tạm của NC (khớp đúng danh sách ảnh gửi). Trang `/du-an/` vẫn tồn tại, vẫn còn link "Dự án tiêu biểu" ở footer. **Còn treo:** đây là quyết định của NC, chưa phải xác nhận chính thức từ Chú Thuận |
| 6 | **Liên hệ** | Giữ nguyên, vẫn là nút CTA cuối navbar | ✅ Không đổi |

> ⚠️ **3 việc còn treo cần Chú Thuận xác nhận trước khi lên production** (đã tạm quyết định theo hướng an toàn nhất để build được ngay, không phải quyết định cuối cùng):
> 1. Đích đến thật của "Giới thiệu" (`/ve-tadic/` hay trang mới).
> 2. Nội dung/trang đích của "Video" (hiện chưa có trong navbar).
> 3. Số phận "Dự án" (bỏ hẳn hay gộp vào mục khác) — hiện đã bỏ khỏi navbar chính, trang gốc vẫn còn.

**Dropdown con của "Giải pháp ứng dụng AI"** (7 mục, đúng theo nội dung ảnh gửi — thay thế cho nội dung dropdown "Giải pháp" cũ):

| # | Tên giải pháp |
|---|---|
| 1 | Khảo sát và quản lý bảo trì đường bộ |
| 2 | Thu thập và quản lý tài sản đường bộ |
| 3 | Giám sát lưu lượng và phân loại phương tiện đường bộ |
| 4 | Giám sát vệ sinh và mỹ quan đường phố |
| 5 | Giám sát công trình xây dựng và nhà máy |
| 6 | Quản trị doanh nghiệp vừa và nhỏ |
| 7 | Số hóa và quản lý hồ sơ |

> Đây là nội dung thuộc phạm vi trang chủ/cấu trúc chung của website (nằm ngoài phạm vi kỹ thuật của module Legal Doc Sync), nhưng ghi lại ở đây để đồng bộ vị trí "Văn bản liên quan" trong navbar tổng thể. **Chưa áp dụng vào code** — xem trạng thái thực tế ở dòng #2 của bảng trên.

**Lý do đặt "Văn bản liên quan" ở vị trí này:** mục "Văn bản liên quan" mang tính chất thông tin/tin tức (nội dung cập nhật định kỳ, không phải trang chuyển đổi/CTA), nên đặt liền kề "Tin tức & sự kiện" là hợp lý về mặt phân nhóm thông tin.

**Việc cần làm trong code (đã hoàn thành, trạng thái theo bảng ở trên):**
- [x] **Xoá dropdown "Sản phẩm"** khỏi `base.html`/navbar component — xoá cả markup lẫn context liên quan, không chỉ ẩn bằng CSS.
- [x] Đổi label "Giải pháp" → "Giải pháp ứng dụng AI" — **chưa** đổi nội dung dropdown con thành 7 mục tĩnh (xem còn treo #2 ở trên).
- [x] Đổi "Trang chủ" + "Về chúng tôi" → gộp thành 1 mục "Giới thiệu", trỏ tạm về `/ve-tadic/` (còn treo #1 ở trên).
- [ ] Thêm mục "Video" mới vào navbar — **chưa làm**, chờ xác nhận nội dung/trang đích (còn treo #2).
- [x] Đổi "Tin tức" → "Tin tức & sự kiện" (label only).
- [x] Đổi thẻ nav "Văn bản liên quan" sang route mới `/van-ban-lien-quan/` (tên kỹ thuật URL Django vẫn là `van_ban_list`, không dùng namespace `legal_docs:` như bản nháp ban đầu — xem mục 15.1).
- [x] Trạng thái **active/highlight** dùng `request.path`, tự động ăn theo `--color-primary` xanh dương mới (mục 14.4) — không cần sửa thêm.
- [x] Responsive: soát lại CSS (`static/css/style.css`) và JS (`static/js/script.js`) — nav dùng `flex` + `gap`, JS `querySelectorAll('.has-dropdown')` động, không hardcode số lượng mục nên bớt 2 mục không vỡ layout. *(Đã soát code, chưa chụp ảnh màn hình mobile thật để xác nhận bằng mắt.)*
- [x] Redirect 301 từ `/van-ban-phap-ly/` sang `/van-ban-lien-quan/` — thêm trong `config/urls.py`.
- [x] **(Phát sinh, không có trong đặc tả gốc)** Route công khai đổi kéo theo 2 endpoint cron cũng trỏ sai nếu không sửa: đã cập nhật `vercel.json` (`crons[0].path`) và `.github/workflows/sync-vanban.yml` (`SYNC_URL`) sang `/van-ban-lien-quan/cron/sync/` — nếu bỏ sót, job đồng bộ tự động 6h/lần (Bước 7, mục 10) sẽ gọi vào URL redirect thay vì endpoint thật.

---

## 16. Ghi chú

Tài liệu này tổng hợp từ trao đổi nội bộ giữa Chú Thuận (yêu cầu nghiệp vụ) và NC (đề xuất phương án kỹ thuật), dùng làm đặc tả đầu vào để build bằng Claude Code / Claude Cowork. Khi vibe-code, nên đi tuần tự theo lộ trình ở mục 10, mỗi bước nên có test đi kèm trước khi ghép vào pipeline tổng (`sync_vanban`).

**Cập nhật gần nhất (2026-08-30):** đã hoàn thành fetch RSS + lọc + lưu DB + cảnh báo optional (skip an toàn khi thiếu credentials) + trang hiển thị **"Văn bản liên quan"** (đổi tên lần 2 từ "Văn bản pháp lý", route mới `/van-ban-lien-quan/`, có redirect 301 từ route cũ) + **phân nhóm nghiệp vụ (mục 6.1)** đầy đủ (cột DB, `phan_nhom()`, backfill, view/template gom theo nhóm, cảnh báo kèm tên nhóm, API filter theo nhóm) + giao diện so le trắng/xanh dương áp dụng cho cả trang chủ lẫn từng nhóm nghiệp vụ + **đổi màu brand `--color-primary` từ xanh lá sang xanh dương `#2559D8`** (mục 14.4) + **xây lại navbar** theo mục 15.2: bỏ hẳn "Sản phẩm" và "Dự án", gộp "Trang chủ"+"Về chúng tôi" → "Giới thiệu", đổi "Giải pháp"→"Giải pháp ứng dụng AI", "Tin tức"→"Tin tức & sự kiện", "Văn bản pháp lý"→"Văn bản liên quan" — navbar thực tế hiện là *Giới thiệu · Giải pháp ứng dụng AI ▾ · Tin tức & sự kiện · Văn bản liên quan · Liên hệ* (**chưa có "Video"** — xem 3 việc còn treo ở mục 15.2).

> Lưu ý minh bạch: các mục "Bước 9/9d/12" ở mục 10 (đã đánh dấu `[x]` từ trước) mô tả đúng *thiết kế dự định*, nhưng tới trước ngày 2026-08-30 code thực tế trong repo (`config/urls.py`, `apps/home/templates/home/base.html`) **vẫn còn dùng route/label cũ `/van-ban-phap-ly/` và "Văn bản pháp lý"** — tài liệu bị lệch so với code tại thời điểm đó. Đã đối chiếu và đồng bộ lại code khớp tài liệu trong đợt cập nhật 2026-08-30 này.

**Việc còn lại:**
- Xử lý tham số API `ws.vbpl.vn` (mục 2).
- Cài `deploy/systemd/tadic-vanban-sync.timer` lên VPS (mục 3.1).
- Chạy `python manage.py backfill_nhom` trên DB production sau khi deploy migration `0002_...`.
- Rà soát toàn site để thay hết các chỗ còn hard-code hex xanh lá cũ ngoài biến `--color-primary`.
- **(MỚI — cần xác nhận với Chú Thuận)** 3 việc còn treo của navbar (mục 15.2): (1) đích đến thật của "Giới thiệu" — hiện tạm trỏ `/ve-tadic/`; (2) nội dung/trang đích cho "Video" — hiện chưa đưa lên navbar; (3) số phận "Dự án" — hiện đã bỏ khỏi navbar chính (trang `/du-an/` vẫn còn, vẫn có link ở footer), nhưng đây là quyết định tạm của NC chứ chưa phải xác nhận chính thức.
- **(MỚI)** Dropdown "Giải pháp ứng dụng AI" hiện vẫn giữ 11 mục động từ DB, chưa đổi thành đúng 7 mục tĩnh theo ảnh gửi — cần Chú Thuận xác nhận trước khi đổi (đổi sai có thể làm mất link 11 trang giải pháp đang có).
- Chưa chụp ảnh/kiểm tra bằng mắt navbar mới trên trình duyệt mobile thật (mới soát code CSS/JS, chưa test trực quan).
