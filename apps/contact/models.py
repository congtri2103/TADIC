from django.db import models


class ContactSubmission(models.Model):
    name             = models.CharField(max_length=100, verbose_name='Họ tên')
    email            = models.EmailField(verbose_name='Email')
    phone            = models.CharField(max_length=20, verbose_name='Số điện thoại')
    organization     = models.CharField(max_length=200, blank=True, verbose_name='Cơ quan')
    product_interest = models.CharField(max_length=50, default='all', verbose_name='Sản phẩm quan tâm')
    message          = models.TextField(blank=True, verbose_name='Nội dung')
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering        = ['-created_at']
        verbose_name    = 'Liên hệ'
        verbose_name_plural = 'Liên hệ'

    def __str__(self):
        return f'{self.name} - {self.email}'
