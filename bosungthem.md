# Legal Doc Sync – Tự động cập nhật văn bản pháp luật Bộ Xây dựng lên website TADIC

> Module tự động thu thập, chuẩn hoá và đồng bộ các văn bản pháp luật (Thông tư, Nghị định, QCVN, TCVN...) do **Bộ Xây dựng (BXD)** ban hành, hiển thị dưới dạng mục "Văn bản pháp lý" trên website công ty và (mở rộng) cấp dữ liệu cho **VRoad.AI** như một module cập nhật pháp lý tự động.

---

## 1. Bối cảnh & mục tiêu

**Vấn đề:** Team cần một trang "Văn bản pháp lý" trên website công ty, liệt kê các văn bản mới ban hành liên quan đến đường bộ / hạ tầng giao thông / xây dựng, luôn cập nhật mà không cần copy-paste thủ công từ `moc.gov.vn`.

**Ràng buộc quan trọng:**
- ❌ **Không crawl trực tiếp HTML của `moc.gov.vn`** — site chặn truy cập tự động theo `robots.txt`. Vi phạm điều khoản sử dụng và dễ bị block IP.
- ✅ Phải dùng các **kênh dữ liệu hợp lệ** (RSS / trang liệt kê chính thức / API có cấu trúc).
- ✅ Sau sự kiện **sáp nhập Bộ GTVT vào Bộ Xây dựng**, toàn bộ văn bản đường bộ (kể cả các Thông tư cũ ký hiệu `-BGTVT`) nay nằm trong hệ thống của BXD. Bộ lọc bắt buộc phải nhận diện **cả hai ký hiệu**: `-BXD` và `-BGTVT`.

**Mục tiêu đầu ra:**
1. Trang web công ty có mục văn bản pháp lý tự cập nhật (không cần admin thao tác thủ công).
2. Dữ liệu có cấu trúc (không phải HTML thô) → có thể tái sử dụng làm module "cập nhật pháp lý tự động" gắn vào **VRoad.AI**, không chỉ dừng ở mục tin trên website.
3. Cảnh báo (Zalo/email) khi có văn bản mới thuộc nhóm từ khoá công ty theo dõi.

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
  → ghi vào PostgreSQL
  → 1) render trang "Văn bản pháp lý" trên website
    2) cảnh báo Zalo/email khi có VB thuộc từ khoá theo dõi (tuỳ chọn, có thể để trống)
```

### 3.1 Lựa chọn đã áp dụng: tích hợp thành Django app

Đã quyết định (xem log trao đổi build): **tích hợp thành Django app mới** trong repo TADIC hiện có — `apps/legal_docs/` (hoặc tên tương đương), dùng ORM Django, management command `sync_vanban`, view render trang `/van-ban-phap-ly` dùng chung `base.html`/design system hiện có. Đồng bộ tự động qua **systemd timer** trên VPS (`deploy/systemd/tadic-vanban-sync.service` + `.timer`, chạy mỗi 6h) — đã tạo file cấu hình, **chưa cài đặt vào server**, để dành cho lần deploy tiếp theo.

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
5. **Lưu trữ** — ghi vào PostgreSQL (bảng `van_ban_phap_luat`, giữ nguyên tên bảng/model kỹ thuật — xem lưu ý đổi tên ở mục 15), có `ngay_thu_thap` để biết lần crawl.
6. **Đầu ra**
   - Render lại trang "Văn bản pháp lý" trên website (view Django đọc trực tiếp từ DB qua ORM).
   - Gửi cảnh báo qua Zalo OA / email nếu văn bản mới khớp từ khoá theo dõi — **tuỳ chọn (optional)**, tự động skip nếu thiếu `ZALO_OA_ACCESS_TOKEN` / `LEGAL_ALERT_EMAIL_TO`, không gây lỗi hệ thống.

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
| `linh_vuc` | text | Lĩnh vực (đường bộ, xây dựng, hạ tầng kỹ thuật...) |
| `trang_thai_hieu_luc` | text (enum) | `Còn hiệu lực` / `Hết hiệu lực` / `Sửa đổi bổ sung` / `Chưa có hiệu lực` |
| `url_goc` | text | Link tới trang chi tiết văn bản (vbpl.vn hoặc moc.gov.vn) |
| `url_file` | text, nullable | Link file đính kèm (PDF/DOC) nếu có |
| `ngay_thu_thap` | timestamp | Thời điểm hệ thống ghi nhận bản ghi này |

```sql
CREATE TABLE van_ban_phap_luat (
    id               BIGSERIAL PRIMARY KEY,
    so_hieu          TEXT NOT NULL,
    loai_vb          TEXT,
    co_quan_ban_hanh TEXT,
    ngay_ban_hanh    DATE,
    ngay_hieu_luc    DATE,
    trich_yeu        TEXT,
    linh_vuc         TEXT,
    trang_thai_hieu_luc TEXT,
    url_goc          TEXT,
    url_file         TEXT,
    ngay_thu_thap    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (so_hieu, ngay_ban_hanh)
);

CREATE INDEX idx_vbpl_linh_vuc ON van_ban_phap_luat (linh_vuc);
CREATE INDEX idx_vbpl_ngay_ban_hanh ON van_ban_phap_luat (ngay_ban_hanh DESC);
```

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

Văn bản khớp từ khoá → gắn cờ `uu_tien = True` → kích hoạt cảnh báo Zalo/email; văn bản không khớp vẫn có thể lưu vào DB nhưng không đẩy lên trang chủ / không cảnh báo (tuỳ cấu hình `linh_vuc` mong muốn hiển thị công khai).

---

## 7. Cảnh báo Zalo / Email (tuỳ chọn — optional)

Khi crawl phát hiện văn bản **mới** (chưa có trong DB) và **khớp từ khoá ưu tiên**:

- **Zalo OA**: gọi thẳng **Zalo OA API** (`openapi.zalo.me/v3.0/oa/message/cs`) bằng `ZALO_OA_ACCESS_TOKEN` + `ZALO_OA_RECIPIENT_ID`. Nếu có cấu hình thêm `ZALO_OA_WEBHOOK_URL` (ví dụ forward qua n8n), hàm sẽ **ưu tiên gửi qua webhook** thay vì gọi API trực tiếp.
- **Email**: gửi qua SMTP nội bộ hoặc dịch vụ (SendGrid/Mailgun) tới danh sách `LEGAL_ALERT_EMAIL_TO`.

**Cơ chế skip an toàn (đã xác nhận, đã sửa trong `notify_zalo.py`):**
- Nếu **`ZALO_OA_ACCESS_TOKEN` trống** → tự động bỏ qua bước gửi Zalo, không lỗi, không chặn pipeline.
- **Không còn bắt buộc** phải có `ZALO_OA_WEBHOOK_URL` — chỉ cần token là đủ để gọi API trực tiếp.
- Tương tự, nếu `LEGAL_ALERT_EMAIL_TO` trống → bỏ qua gửi email.

Nội dung cảnh báo tối thiểu: `so_hieu`, `trich_yeu`, `ngay_ban_hanh`, `ngay_hieu_luc`, `url_goc`.

---

## 8. Hiển thị trên website công ty

- Trang **`/van-ban-phap-ly`** (đổi từ `/van-ban-phap-luat` — xem lý do đổi tên ở mục 15), dùng chung `base.html`/design system hiện có của website TADIC, view Django đọc trực tiếp từ PostgreSQL qua ORM.
- Mỗi văn bản hiển thị: số hiệu, loại VB, trích yếu, ngày ban hành, trạng thái hiệu lực (badge màu), link file/link gốc.
- Có thể thêm bộ lọc phía client theo `linh_vuc` hoặc theo trạng thái hiệu lực.
- **Thêm mục "Văn bản pháp lý" vào thanh điều hướng chính (navbar)** — xem chi tiết mục 15.

---

## 9. Mở rộng: module cho VRoad.AI

Giá trị cộng thêm quan trọng nhất của hệ thống này: đây không chỉ là "mục tin tức" trên website, mà là **mảnh ghép "cập nhật pháp lý tự động"** có thể gắn thẳng vào **VRoad.AI** như một module nghiệp vụ — ví dụ: tự động đối chiếu quy chuẩn/định mức bảo trì đường bộ mới nhất khi VRoad.AI tính toán chỉ số IRI, phân cấp mức độ hư hỏng hoặc lập kế hoạch bảo trì.

Vì dữ liệu đã được chuẩn hoá schema (mục 4) và lưu trong PostgreSQL, việc tích hợp chỉ cần expose thêm 1 API nội bộ (`GET /api/vanban?linh_vuc=...&trang_thai=...`) để VRoad.AI gọi tới — không cần xây lại pipeline crawl riêng.

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
- [ ] **Bước 9 — Trang hiển thị** `/van-ban-phap-ly` — cần đổi route + label theo mục 15, kiểm tra hiển thị đúng design.
- [ ] **Bước 10 — (Mở rộng)** Expose API nội bộ cho VRoad.AI đọc dữ liệu văn bản.
- [ ] **Bước 11 — (Mới) Giao diện màu so le trắng/xanh** cho các section trang chủ/trang văn bản pháp lý — xem mục 14.
- [ ] **Bước 12 — (Mới) Đổi tên hiển thị** "Văn bản pháp luật" → "Văn bản pháp lý" trên UI + thêm mục này vào navbar chính — xem mục 15.

---

## 11. Cấu trúc thư mục thực tế (đã tích hợp vào repo TADIC)

```
TADIC/                                # Repo Django hiện có của công ty
├── apps/
│   ├── home/
│   └── legal_docs/                   # App mới cho module này
│       ├── management/
│       │   └── commands/
│       │       └── sync_vanban.py    # Entry point: fetch → chuẩn hoá → dedupe → lọc → lưu DB
│       ├── models.py                 # Model VanBanPhapLuat (map schema mục 4)
│       ├── views.py                  # View render trang /van-ban-phap-ly
│       ├── fetch_rss.py
│       ├── fetch_vbpl_api.py
│       ├── normalize.py
│       ├── filters.py                # la_van_ban_bxd(), khop_tu_khoa()
│       ├── dedupe.py
│       ├── notify_zalo.py
│       ├── notify_email.py
│       └── migrations/
├── templates/
│   └── legal_docs/
│       └── van_ban_phap_ly.html      # Dùng chung base.html hiện có
├── deploy/
│   └── systemd/
│       ├── tadic-vanban-sync.service
│       └── tadic-vanban-sync.timer
├── tests/
│   ├── test_filters.py
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

# Legal Doc Sync — Văn bản pháp lý
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

---

## 13. Rủi ro & lưu ý khi triển khai

| Rủi ro | Giải pháp |
|---|---|
| API `ws.vbpl.vn` chưa xác định rõ contract (endpoint/tham số/auth), hiện trả 0 kết quả | Soi request thật qua DevTools trên `vbpl.vn` khi tra cứu thủ công; đăng ký tài khoản CSDLQG nếu cần xác thực. Không chặn MVP vì RSS đã đủ dùng |
| RSS đổi cấu trúc / đổi URL | Bọc `fetch_rss.py` bằng try/except, log lỗi, không để job chết toàn bộ pipeline |
| Trùng lặp văn bản do sai khác nhỏ ở số hiệu (khoảng trắng, hoa/thường) | Chuẩn hoá `so_hieu` (strip, upper-case phần ký hiệu) trước khi dùng làm khoá dedupe |
| Văn bản GTVT cũ bị bỏ sót do chỉ lọc `-BXD` | Đã xử lý ở mục 5 — luôn test cả 2 pattern `-BXD` và `-BGTVT` |
| Cảnh báo spam khi lần đầu chạy job với DB rỗng | Thêm cờ "first run" — lần chạy đầu tiên chỉ ghi dữ liệu, không gửi cảnh báo hàng loạt |
| Vi phạm robots.txt nếu vô tình fallback sang crawl HTML | Không implement bất kỳ HTML scraper nào cho `moc.gov.vn`; nếu thiếu dữ liệu, ưu tiên bổ sung qua API/RSS hoặc liên hệ xin quyền truy cập chính thức |
| Zalo OA access token hết hạn (token ngắn hạn) | Cần xử lý refresh token nếu dùng lâu dài — kiểm tra `notify_zalo.py` đã hỗ trợ refresh chưa, nếu chưa thì thêm sau |
| `.env` thật (`SERVER_IP`, SMTP, Zalo token...) bị commit nhầm vào Git | Đảm bảo `.env` nằm trong `.gitignore`, chỉ dùng `.env.example`/`.env.vps.example` làm mẫu công khai |

---

## 14. Yêu cầu bổ sung — Giao diện: màu nền so le trắng/xanh

**Bối cảnh:** tham khảo phong cách landing page dạng "Base CRM" (ảnh minh hoạ đính kèm trong trao đổi nội bộ) — các section trên trang được **so le nền trắng và nền xanh đậm (brand color)** liên tiếp nhau, tạo nhịp thị giác rõ ràng khi cuộn trang, thay vì toàn bộ nền trắng đơn điệu như hiện tại.

### 14.1 Nguyên tắc áp dụng

- Chia trang thành các **section khối lớn** theo chiều dọc (hero, giới thiệu, dịch vụ/giải pháp, dự án nổi bật, CTA liên hệ...).
- Áp màu nền **so le**: section 1 trắng → section 2 xanh đậm (brand) → section 3 trắng → section 4 xanh đậm... (không cố định thứ tự tuyệt đối, miễn xen kẽ, tránh 2 section cùng màu liền kề).
- Khi nền là xanh đậm: chữ chuyển sang **trắng/màu sáng** để đảm bảo tương phản (không giữ nguyên chữ đen trên nền xanh đậm).
- Không đổi màu tổng thể `body`/`header` cố định — chỉ đổi nền theo từng `<section>`, để header/navbar vẫn nhất quán khi cuộn qua nhiều section màu khác nhau (dùng nền trong suốt hoặc nền riêng cố định cho `<nav>`).

### 14.2 Cách làm kỹ thuật (CSS variables — tái sử dụng design system hiện có)

Không tạo màu mới tuỳ tiện — tái sử dụng biến màu thương hiệu đã khai báo sẵn trong `variables.css` của website (`--color-primary` hoặc tương đương, hiện là tông xanh theo logo/nút "Liên hệ" trên navbar thực tế của TADIC).

```css
/* variables.css — bổ sung nếu chưa có */
:root {
  --section-bg-light: #FFFFFF;
  --section-bg-dark: var(--color-primary);      /* dùng lại xanh thương hiệu hiện có, KHÔNG hard-code hex mới */
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
- Trang **`/van-ban-phap-ly`** (module đang build): danh sách văn bản dùng nền trắng là chính (dễ đọc bảng dữ liệu dài), chỉ phần **hero/tiêu đề đầu trang** áp `section--dark` cho đồng bộ phong cách toàn site.
- Không bắt buộc áp cho các trang nội dung dài khác (Tin tức, chi tiết dự án...) trong đợt này — có thể mở rộng sau nếu duyệt hiệu ứng ổn trên trang chủ.

---

## 15. Yêu cầu bổ sung — Đổi tên & thêm mục vào thanh điều hướng

### 15.1 Đổi tên hiển thị: "Văn bản pháp luật" → "Văn bản pháp lý"

> **Lưu ý thuật ngữ:** "Văn bản pháp luật" là cách gọi chuẩn xác hơn về mặt pháp lý (đúng thuật ngữ hành chính). "Văn bản pháp lý" là cách gọi phổ thông, ngắn gọn, dễ đọc hơn trên UI. Đây là lựa chọn về mặt thương hiệu/UX của TADIC, không phải lỗi sai — giữ nguyên theo yêu cầu.

**Phạm vi đổi tên (chỉ đổi phần hiển thị cho người dùng, KHÔNG đổi tên kỹ thuật nội bộ để tránh phá vỡ dữ liệu/migration đã có):**

| Vị trí | Trước | Sau |
|---|---|---|
| Label trên navbar | *(chưa có)* | **Văn bản pháp lý** |
| Tiêu đề trang (`<h1>`, `<title>`) | Văn bản pháp luật | Văn bản pháp lý |
| URL / route | `/van-ban-phap-luat` | `/van-ban-phap-ly` |
| Breadcrumb, meta description | Văn bản pháp luật | Văn bản pháp lý |

**Giữ nguyên (không đổi), vì là tên kỹ thuật nội bộ, đổi sẽ tốn công migrate không cần thiết:**
- Tên bảng DB: `van_ban_phap_luat`
- Tên app Django: `legal_docs`
- Tên model: `VanBanPhapLuat`
- Tên biến môi trường: `LEGAL_ALERT_EMAIL_TO`, `MOC_RSS_URL`...

> Nếu route cũ `/van-ban-phap-luat` đã từng được chia sẻ/index bởi Google trước đó, cân nhắc thêm `redirect 301` từ route cũ sang route mới để không mất SEO — việc này chỉ cần thiết nếu trang đã lên production trước khi đổi tên.

### 15.2 Thêm mục vào thanh điều hướng chính (navbar)

Theo cấu trúc navbar thực tế hiện có của website TADIC:

```
Trang chủ · Về chúng tôi · Giải pháp ▾ · Sản phẩm ▾ · Dự án · Tin tức · [Liên hệ →]
```

➡️ Thêm **"Văn bản pháp lý"** vào giữa **"Tin tức"** và nút **"Liên hệ"**:

```
Trang chủ · Về chúng tôi · Giải pháp ▾ · Sản phẩm ▾ · Dự án · Tin tức · Văn bản pháp lý · [Liên hệ →]
```

**Lý do đặt vị trí này:** mục "Văn bản pháp lý" mang tính chất thông tin/tin tức (giống "Tin tức" về bản chất — nội dung cập nhật định kỳ, không phải trang chuyển đổi/CTA), nên đặt liền kề "Tin tức" là hợp lý về mặt phân nhóm thông tin, đồng thời không chen vào giữa nhóm "Giải pháp/Sản phẩm/Dự án" vốn là các mục giới thiệu năng lực cốt lõi của công ty.

**Việc cần làm trong code:**
- Thêm 1 thẻ `<a href="{% url 'legal_docs:list' %}">Văn bản pháp lý</a>` (hoặc tương đương theo cách navbar hiện đang được render — kiểm tra `base.html`/`navbar` component hiện có là hardcode HTML hay loop qua danh sách menu item trong context/settings).
- Đảm bảo trạng thái **active/highlight** đúng khi đang ở trang `/van-ban-phap-ly` (theo cùng cơ chế đang dùng cho các mục khác, ví dụ so khớp `request.path`).
- Kiểm tra responsive: mục mới không làm vỡ layout navbar trên mobile (nếu navbar hiện tại chuyển sang dạng hamburger menu ở màn hình nhỏ, mục mới cũng phải nằm đúng trong menu đó).

---

## 16. Ghi chú

Tài liệu này tổng hợp từ trao đổi nội bộ giữa Chú Thuận (yêu cầu nghiệp vụ) và NC (đề xuất phương án kỹ thuật), dùng làm đặc tả đầu vào để build bằng Claude Code / Claude Cowork. Khi vibe-code, nên đi tuần tự theo lộ trình ở mục 10, mỗi bước nên có test đi kèm trước khi ghép vào pipeline tổng (`sync_vanban`).

**Cập nhật gần nhất:** đã hoàn thành fetch RSS + lọc + lưu DB + cảnh báo optional (skip an toàn khi thiếu credentials). Việc còn lại: xử lý tham số API `ws.vbpl.vn`, hoàn thiện trang hiển thị theo tên mới **"Văn bản pháp lý"**, áp dụng giao diện màu so le trắng/xanh, và thêm mục vào navbar chính (mục 14, 15).