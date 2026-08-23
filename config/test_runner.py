"""Test runner cho layout `apps/` nằm trên sys.path.

`config.settings` thêm `BASE_DIR/apps` vào sys.path nên các app được import
bằng tên top-level (`home`, `legalvb`, ...). Nếu để `manage.py test` tự dò từ
thư mục gốc, unittest sẽ import lại chính module đó dưới tên `apps.legalvb.*`
và Django báo lỗi "Model class ... doesn't declare an explicit app_label".

Runner này mặc định chỉ dò trong các app cục bộ (theo đúng tên top-level).
"""

from django.apps import apps as django_apps
from django.conf import settings
from django.test.runner import DiscoverRunner


def _local_app_labels():
    apps_dir = settings.BASE_DIR / 'apps'
    return [
        cfg.name
        for cfg in django_apps.get_app_configs()
        if str(cfg.path).startswith(str(apps_dir))
    ]


class AppsDiscoverRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, **kwargs):
        if not test_labels:
            test_labels = _local_app_labels()
        return super().build_suite(test_labels, **kwargs)
