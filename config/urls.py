from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('contact/', include('contact.urls')),
    path('career/', include('career.urls')),
    path('van-ban-lien-quan/', include('legalvb.urls')),
    # Route cũ trước khi đổi tên hiển thị "Văn bản pháp lý" → "Văn bản liên quan"
    # (mục 15.1) — giữ redirect 301 để không mất SEO/link đã chia sẻ.
    path('van-ban-phap-ly/', RedirectView.as_view(url='/van-ban-lien-quan/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
