"""Build command cho Vercel (khai báo trong vercel.json → buildCommand).

Vercel tự nhận diện Django và tự chạy `collectstatic`, nhưng KHÔNG chạy
`migrate` và cũng không có cách nào chạy lệnh một lần trên môi trường
production (không SSH, `DATABASE_URL` bị đánh dấu Sensitive nên không pull
về máy được). Vì vậy các bước khởi tạo DB được gắn vào chính build.

- migrate: luôn chạy, LỖI THÌ DỪNG BUILD (thà không deploy còn hơn deploy một
  bản chắc chắn 500).
- seed: chỉ chạy cho những bảng đang RỖNG. Các lệnh seed dùng
  `update_or_create` nên nếu chạy vô điều kiện mỗi lần deploy sẽ ghi đè nội
  dung biên tập viên sửa trong CMS — cổng "chỉ seed khi rỗng" khiến chúng tự
  tắt ngay sau lần khởi tạo đầu tiên.
- sync_vanban: chạy khi bảng văn bản còn rỗng (nạp lần đầu), hoặc khi ép bằng
  VANBAN_SYNC_ON_BUILD=1. Không bao giờ làm hỏng build — nguồn ws.vbpl.vn /
  RSS Bộ Xây dựng có thể timeout. Cập nhật định kỳ do Vercel Cron đảm nhiệm.
"""

import os
import subprocess
import sys


def run(args, *, required):
    print(f'[vercel_build] $ manage.py {" ".join(args)}', flush=True)
    result = subprocess.run([sys.executable, 'manage.py', *args])
    if result.returncode != 0:
        if required:
            sys.exit(result.returncode)
        print(f'[vercel_build] bỏ qua lỗi (không bắt buộc): {args[0]}', flush=True)


def seed_empty_tables():
    """Seed dữ liệu khởi tạo cho những bảng chưa có bản ghi nào."""
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    from home.management.commands.seed_products import PRODUCTS
    from home.models import NewsArticle, Partner, Product, Project, Stat, Testimonial
    from legalvb.models import VanBanPhapLuat

    missing_keys = {p['key'] for p in PRODUCTS} - set(
        Product.objects.values_list('key', flat=True)
    )
    if missing_keys:
        print(f'[vercel_build] thiếu {len(missing_keys)} product: '
              f'{", ".join(sorted(missing_keys))}', flush=True)
        run(['seed_products'], required=False)

    # seed_data nạp cả 5 model này cùng lúc, nên chỉ chạy khi TẤT CẢ đều rỗng
    # (DB mới tinh) — tránh ghi đè khi mới chỉ một bảng bị thiếu.
    content_models = (NewsArticle, Project, Testimonial, Partner, Stat)
    counts = {M.__name__: M.objects.count() for M in content_models}
    if not any(counts.values()):
        print('[vercel_build] chưa có nội dung nào — chạy seed_data.', flush=True)
        run(['seed_data'], required=False)
    else:
        print(f'[vercel_build] đã có nội dung {counts} — bỏ qua seed_data.', flush=True)

    # Nạp lần đầu cho DB mới; sau đó Vercel Cron (crons trong vercel.json) lo
    # việc cập nhật định kỳ nên build không cần đụng tới nữa.
    if not VanBanPhapLuat.objects.exists():
        print('[vercel_build] chưa có văn bản pháp lý nào — chạy sync_vanban.', flush=True)
        run(['sync_vanban'], required=False)


def main():
    if not os.environ.get('DATABASE_URL'):
        # Preview build không có DATABASE_URL (biến chỉ set cho Production);
        # migrate lên sqlite tạm trong sandbox build là vô nghĩa.
        print('[vercel_build] DATABASE_URL chưa set — bỏ qua migrate.', flush=True)
        return

    run(['migrate', '--noinput'], required=True)
    seed_empty_tables()

    if os.environ.get('VANBAN_SYNC_ON_BUILD', '').strip().lower() in {'1', 'true', 'yes', 'on'}:
        run(['sync_vanban'], required=False)


if __name__ == '__main__':
    main()
