from django.db import models


class VanBanPhapLuat(models.Model):
    TRANG_THAI_CHOICES = [
        ('con_hieu_luc',     'Còn hiệu lực'),
        ('het_hieu_luc',     'Hết hiệu lực'),
        ('sua_doi_bo_sung',  'Sửa đổi bổ sung'),
        ('chua_co_hieu_luc', 'Chưa có hiệu lực'),
        ('khong_ro',         'Không rõ'),
    ]
    NGUON_CHOICES = [
        ('vbpl_api', 'API vbpl.vn'),
        ('moc_rss',  'RSS Bộ Xây dựng'),
    ]

    so_hieu              = models.CharField(max_length=100)
    loai_vb              = models.CharField(max_length=100, blank=True)
    co_quan_ban_hanh     = models.CharField(max_length=200, blank=True)
    ngay_ban_hanh        = models.DateField(null=True, blank=True)
    ngay_hieu_luc        = models.DateField(null=True, blank=True)
    trich_yeu            = models.TextField()
    linh_vuc             = models.CharField(max_length=200, blank=True)
    trang_thai_hieu_luc  = models.CharField(max_length=30, choices=TRANG_THAI_CHOICES, default='khong_ro')
    url_goc              = models.URLField(max_length=500, blank=True)
    url_file             = models.URLField(max_length=500, blank=True)
    nguon                = models.CharField(max_length=20, choices=NGUON_CHOICES)
    uu_tien              = models.BooleanField(default=False)
    nhom_nghiep_vu_id     = models.CharField(max_length=50, blank=True, null=True)
    nhom_nghiep_vu_label  = models.CharField(max_length=100, blank=True, null=True)
    hien_thi             = models.BooleanField(default=True)
    da_canh_bao          = models.BooleanField(default=False)
    ngay_thu_thap        = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['so_hieu', 'ngay_ban_hanh'], name='uniq_sohieu_ngaybanhanh'),
        ]
        ordering = ['-ngay_ban_hanh']
        indexes = [
            models.Index(fields=['linh_vuc']),
            models.Index(fields=['-ngay_ban_hanh']),
            models.Index(fields=['nhom_nghiep_vu_id']),
        ]

    def __str__(self):
        return f'{self.so_hieu} — {self.trich_yeu[:60]}'
