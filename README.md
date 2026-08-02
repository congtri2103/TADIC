# TADIC.AI — Nền tảng Quản lý & Bảo trì Hạ tầng Giao thông bằng AI

<div align="center">

![TADIC Logo](https://img.shields.io/badge/TADIC-AI%20Road%20Tech-2563eb?style=for-the-badge&logo=road&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

**Công ty Cổ phần Xây dựng và Công nghệ TADIC**  
*Giải pháp AI toàn diện cho quản lý, giám sát và bảo trì hạ tầng giao thông đường bộ*

</div>

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Cài đặt & Chạy thử](#-cài-đặt--chạy-thử)
- [Biến môi trường](#-biến-môi-trường)
- [Seed dữ liệu](#-seed-dữ-liệu)
- [Hệ thống phân quyền (RBAC)](#-hệ-thống-phân-quyền-rbac)
- [API Endpoints](#-api-endpoints)
- [Deploy Production](#-deploy-production)
- [Accounts mặc định](#-accounts-mặc-định)

---

## 🚀 Giới thiệu

**TADIC.AI** là website giới thiệu sản phẩm và cổng thông tin của Công ty Cổ phần Xây dựng và Công nghệ TADIC — đơn vị tiên phong ứng dụng Trí tuệ nhân tạo (AI) vào quản lý, khảo sát và bảo trì hạ tầng giao thông đường bộ tại Việt Nam.

Hệ thống bao gồm:
- **Trang web công khai** — Giới thiệu 14 tác nhân AI, dự án tiêu biểu, tin tức và form liên hệ
- **CMS nội bộ** — Hệ thống quản lý nội dung với phân quyền 6 cấp độ
- **Contact API** — Nhận và lưu trữ yêu cầu tư vấn, tùy chọn gửi email thông báo

---

## ✨ Tính năng

### Trang web công khai
| Tính năng | Mô tả |
|---|---|
| 🤖 **14 Tác nhân AI** | Hiển thị theo 3 nhóm: Giám sát đường bộ, An toàn giao thông, Tự động hóa quy trình |
| 📊 **Thống kê động** | Counter animation cho các chỉ số (km đường, khách hàng, độ chính xác...) |
| 📰 **Tin tức & Blog** | Bài viết chuyên sâu về AI và hạ tầng giao thông |
| 🏗️ **Dự án tiêu biểu** | Gallery masonry với lightbox |
| 💬 **Đánh giá khách hàng** | Carousel testimonials tự động |
| 🌐 **Đối tác** | Marquee logo partners chạy tự động |
| 📬 **Form liên hệ** | Modal form gửi AJAX, lưu DB + email notify |
| 🌙 **Dark/Light mode** | Toggle theme sáng/tối |
| 🔍 **SEO đầy đủ** | Meta tags, OG tags, semantic HTML |
| 📱 **Responsive** | Tương thích mọi thiết bị |

### CMS Nội bộ (`/career/`)
| Tính năng | Mô tả |
|---|---|
| 🔐 **Đăng nhập bảo mật** | CSRF protection, session-based auth |
| 👥 **RBAC 6 cấp** | root / admin / editor / author / reviewer / viewer |
| 📦 **CRUD Sản phẩm** | Quản lý 14 tác nhân AI |
| 📝 **CRUD Tin tức** | Soạn thảo bài viết, publish/unpublish |
| 🗂️ **CRUD Dự án** | Quản lý dự án tiêu biểu |
| 📥 **Inbox Liên hệ** | Xem và xóa yêu cầu tư vấn |
| 👤 **Quản lý User** | Tạo/sửa/xóa tài khoản và phân quyền |

---

## 🛠 Công nghệ sử dụng

| Layer | Công nghệ | Phiên bản |
|---|---|---|
| Backend | Django | 6.0.7 |
| Python | CPython | 3.11+ |
| Database | SQLite (dev) / PostgreSQL (prod) | — |
| Frontend CSS | Vanilla CSS (38KB) | — |
| Frontend JS | Vanilla JS + minified (30KB) | — |
| Fonts | Google Fonts (Inter + Poppins) | — |
| Icons | Font Awesome | 6.5.1 |
| Deploy | Gunicorn + Nginx | — |

---

## 📁 Cấu trúc dự án

```
Web_tadic/
│
├── manage.py                        # Django entry point
├── requirements.txt                 # Python dependencies
├── .env                             # Biến môi trường (không commit)
├── .env.production.example          # Template .env cho production
├── .gitignore
│
├── config/                          # Cấu hình Django
│   ├── settings.py                  # Settings chính
│   ├── urls.py                      # Root URL config
│   ├── wsgi.py                      # WSGI server
│   └── asgi.py                      # ASGI server
│
├── apps/                            # Django applications
│   ├── home/                        # App trang chủ
│   │   ├── models.py                # Product, NewsArticle, Project, Testimonial, Partner, Stat
│   │   ├── views.py                 # Homepage view
│   │   ├── admin.py                 # Django admin
│   │   ├── urls.py
│   │   ├── templates/home/
│   │   │   ├── base.html            # Base template (navbar + footer + modals)
│   │   │   └── index.html           # Trang chủ động
│   │   └── management/commands/
│   │       ├── seed_products.py     # Seed 14 tác nhân AI
│   │       └── seed_data.py         # Seed News, Projects, Testimonials, Partners, Stats
│   │
│   ├── contact/                     # App liên hệ
│   │   ├── models.py                # ContactSubmission
│   │   ├── views.py                 # POST /contact/submit/ API
│   │   ├── admin.py
│   │   └── urls.py
│   │
│   └── career/                      # App CMS nội bộ
│       ├── models.py                # EmployeeProfile (RBAC)
│       ├── forms.py                 # LoginForm, ProductForm, NewsForm, ProjectForm, UserForm
│       ├── views.py                 # Dashboard + CRUD views
│       ├── admin.py
│       ├── urls.py
│       └── templates/career/
│           ├── login.html           # Trang đăng nhập
│           ├── dashboard.html       # Dashboard tổng quan
│           ├── cms_base.html        # Layout CMS (sidebar + topbar)
│           └── cms/
│               ├── product_list.html / product_form.html
│               ├── news_list.html / news_form.html
│               ├── project_list.html / project_form.html
│               ├── contact_list.html
│               └── user_list.html / user_form.html
│
├── static/                          # Static files
│   ├── css/style.css               # CSS đầy đủ (38KB)
│   └── js/script.js                # JavaScript đầy đủ (30KB)
│
├── staticfiles/                     # (auto-generated) collectstatic output
│
├── interface/                       # Giao diện tĩnh gốc (tham khảo)
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── Django/                          # Tài liệu giai đoạn (tham khảo)
    └── Giadoan1/
        ├── index.html               # Template gốc
        └── seed_*.py                # Seed scripts gốc
```

---

## ⚙️ Cài đặt & Chạy thử

### Yêu cầu
- Python 3.11+
- pip
- (Tùy chọn) PostgreSQL nếu deploy production

### 1. Clone & tạo môi trường ảo

```bash
cd /path/to/Web_tadic
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình môi trường

```bash
cp .env.production.example .env    # Nếu chưa có .env
# Chỉnh sửa .env theo nhu cầu
```

File `.env` tối thiểu cho development:
```env
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Chạy migration & seed dữ liệu

```bash
python manage.py migrate
python manage.py seed_products      # 14 tác nhân AI
python manage.py seed_data          # News, Projects, Testimonials, Partners, Stats
```

### 5. Tạo tài khoản admin

```bash
python manage.py createsuperuser
```

### 6. Khởi động server

```bash
python manage.py runserver 8085
```

Mở trình duyệt: **http://localhost:8085**

---

## 🔐 Biến môi trường

| Biến | Mô tả | Mặc định |
|---|---|---|
| `DJANGO_SECRET_KEY` | Secret key bảo mật | (bắt buộc khi production) |
| `DJANGO_DEBUG` | Chế độ debug | `True` |
| `DJANGO_ALLOWED_HOSTS` | Danh sách host cho phép | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origins tin cậy cho CSRF | — |
| `DATABASE_URL` | URL kết nối PostgreSQL | SQLite nếu không set |
| `EMAIL_HOST` | SMTP server | (tùy chọn) |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | SMTP username | — |
| `EMAIL_HOST_PASSWORD` | SMTP password | — |
| `DEFAULT_FROM_EMAIL` | Email gửi đi | `TADIC <noreply@tadic.vn>` |
| `ADMIN_NOTIFY_EMAIL` | Email nhận thông báo liên hệ mới | — |

> **Ghi chú:** Nếu không cấu hình `EMAIL_HOST`, Django sẽ in email ra console (safe cho development).

---

## 🌱 Seed dữ liệu

```bash
# Seed 14 tác nhân AI (Product)
python manage.py seed_products

# Seed nội dung (chạy 1 lần)
python manage.py seed_data
# → 3 bài NewsArticle
# → 4 Project tiêu biểu
# → 3 Testimonials
# → 6 Partners
# → 4 Stats (counter)
```

Để seed lại từ đầu (reset dữ liệu):
```bash
python manage.py flush --no-input
python manage.py seed_products
python manage.py seed_data
```

---

## 👥 Hệ thống phân quyền (RBAC)

Mô hình `EmployeeProfile` gắn với `User` Django, định nghĩa 6 cấp độ theo thứ bậc:

| Role | Cấp | Quyền |
|---|---|---|
| `root` | 100 | Toàn quyền tuyệt đối, quản lý Root khác |
| `admin` | 80 | CRUD tất cả, quản lý User (không xóa Root) |
| `editor` | 60 | CRUD + publish/activate nội dung |
| `author` | 40 | Tạo và sửa nội dung của mình |
| `reviewer` | 20 | Xem và phê duyệt nội dung |
| `viewer` | 0 | Chỉ xem dashboard, không chỉnh sửa |

### Tạo user mới với role:

```bash
python manage.py shell -c "
from django.contrib.auth.models import User
from career.models import EmployeeProfile
u = User.objects.create_user('ten_user', password='mat_khau')
EmployeeProfile.objects.create(user=u, role='editor')
"
```

---

## 🔌 API Endpoints

### Contact Submit
```
POST /contact/submit/
Content-Type: application/json
X-CSRFToken: <csrf_token>

Body:
{
    "name": "Nguyễn Văn A",
    "email": "email@congty.vn",
    "phone": "0901234567",
    "organization": "Sở GTVT Hà Nội",    // optional
    "product_interest": "road-vision-ai",  // optional
    "message": "Nội dung yêu cầu..."       // optional
}

Response 200:
{
    "success": true,
    "message": "Cảm ơn Nguyễn Văn A! Yêu cầu tư vấn đã được ghi nhận."
}

Response 400:
{
    "error": "Vui lòng nhập họ tên."
}
```

### CMS Routes
| URL | Mô tả | Quyền tối thiểu |
|---|---|---|
| `GET /career/login/` | Trang đăng nhập | — |
| `GET /career/dashboard/` | Dashboard tổng quan | viewer |
| `GET /career/cms/products/` | Danh sách sản phẩm | viewer |
| `GET/POST /career/cms/products/add/` | Thêm sản phẩm | author |
| `GET/POST /career/cms/products/<pk>/edit/` | Sửa sản phẩm | author |
| `GET /career/cms/products/<pk>/delete/` | Xóa sản phẩm | admin |
| `GET /career/cms/news/` | Danh sách tin tức | viewer |
| `GET /career/cms/contacts/` | Hộp thư liên hệ | viewer |
| `GET /career/users/` | Quản lý user | admin |
| `GET /admin/` | Django Admin | superuser |

---

## 🚀 Deploy Production

### Yêu cầu server
- Ubuntu 22.04 / Debian 12
- Python 3.11+
- Nginx
- PostgreSQL 14+
- Certbot (SSL)

### Cài đặt

```bash
# 1. Clone project
git clone <repo_url> /var/www/tadic
cd /var/www/tadic

# 2. Tạo môi trường ảo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# 3. Cấu hình .env production
cp .env.production.example .env
nano .env   # Điền đầy đủ thông tin

# 4. Migrate & Seed
python manage.py migrate
python manage.py seed_products
python manage.py seed_data
python manage.py createsuperuser
python manage.py collectstatic --noinput

# 5. Chạy kiểm tra
python manage.py check --deploy
```

### Gunicorn service (`/etc/systemd/system/tadic.service`)

```ini
[Unit]
Description=TADIC Django App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/tadic
Environment="PATH=/var/www/tadic/.venv/bin"
ExecStart=/var/www/tadic/.venv/bin/gunicorn config.wsgi:application \
    --workers 3 \
    --bind 127.0.0.1:8085 \
    --timeout 60 \
    --log-file /var/log/tadic/gunicorn.log \
    --access-logfile /var/log/tadic/access.log

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable tadic
systemctl start tadic
```

### Nginx config (`/etc/nginx/sites-available/tadic`)

```nginx
server {
    listen 80;
    server_name tadic.vn www.tadic.vn;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tadic.vn www.tadic.vn;

    ssl_certificate     /etc/letsencrypt/live/tadic.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tadic.vn/privkey.pem;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/tadic/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/tadic/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8085;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL với Certbot

```bash
certbot --nginx -d tadic.vn -d www.tadic.vn
```

### Backup PostgreSQL định kỳ

```bash
# Thêm vào crontab: crontab -e
0 2 * * * pg_dump tadic_db | gzip > /backups/tadic_$(date +\%Y\%m\%d).sql.gz
```

---

## 🔑 Accounts mặc định

> ⚠️ **Thay đổi mật khẩu trước khi deploy production!**

| Username | Mật khẩu | Role | Quyền |
|---|---|---|---|
| `admin` | `admin2026@tadic` | root | Superuser + Django Admin |
| `root_user` | `root123` | root | Toàn quyền |
| `editor_user` | `edit123` | editor | CRUD + publish |
| `author_user` | `auth123` | author | Tạo/sửa nội dung |
| `viewer_user` | `view123` | viewer | Xem dashboard |

### Đổi mật khẩu:
```bash
python manage.py changepassword admin
```

---

## 📊 Dữ liệu sau khi seed

| Model | Số bản ghi |
|---|---|
| Product (Tác nhân AI) | **14** |
| NewsArticle | **3** |
| Project | **4** |
| Testimonial | **3** |
| Partner | **6** |
| Stat | **4** |
| **Tổng** | **34** |

---

## 🐛 Troubleshooting

### Lỗi `TemplateSyntaxError`
```bash
python manage.py check   # Kiểm tra cấu hình
```

### Lỗi `staticfiles not found`
```bash
python manage.py collectstatic --noinput
```

### Reset database hoàn toàn
```bash
python manage.py flush --no-input
python manage.py migrate
python manage.py seed_products
python manage.py seed_data
```

### Kiểm tra log Gunicorn
```bash
tail -f /var/log/tadic/gunicorn.log
```

---

## 📞 Liên hệ

**Công ty Cổ phần Xây dựng và Công nghệ TADIC**

- 📍 Tầng 12, Tòa nhà Innovation, 123 Đường Láng, Q. Đống Đa, Hà Nội
- 📧 contact@tadic.vn
- ☎️ (024) 3812 3456
- 🌐 www.tadic.vn

---

<div align="center">

© 2026 Công ty Cổ phần Xây dựng và Công nghệ TADIC. All rights reserved.

</div>
