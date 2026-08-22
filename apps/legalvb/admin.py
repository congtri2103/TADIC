from django.contrib import admin

from .models import VanBanPhapLuat


@admin.register(VanBanPhapLuat)
class VanBanPhapLuatAdmin(admin.ModelAdmin):
    list_display  = ('so_hieu', 'trich_yeu', 'ngay_ban_hanh', 'trang_thai_hieu_luc', 'uu_tien', 'hien_thi', 'nguon')
    list_filter   = ('trang_thai_hieu_luc', 'uu_tien', 'hien_thi', 'nguon')
    search_fields = ('so_hieu', 'trich_yeu')
    ordering      = ('-ngay_ban_hanh',)
