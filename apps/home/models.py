from django.db import models
from django.conf import settings
from django.urls import reverse


class Product(models.Model):
    KIND_CHOICES = [
        ('solution', 'Giải pháp AI'),
        ('product', 'Sản phẩm'),
    ]
    CATEGORY_CHOICES = [
        ('road_network', 'Giám sát Mạng lưới Đường bộ'),
        ('road_safety',  'An toàn Giao thông'),
        ('workflow',     'Tự động hóa Quy trình'),
    ]
    STATUS_CHOICES = [
        ('live',        'Live'),
        ('beta',        'Beta'),
        ('coming_soon', 'Sắp ra mắt'),
    ]

    key            = models.SlugField(unique=True)
    kind           = models.CharField(max_length=20, choices=KIND_CHOICES, default='solution')
    title          = models.CharField(max_length=200)
    subtitle       = models.CharField(max_length=200)
    icon           = models.CharField(max_length=50)
    tag            = models.CharField(max_length=50)
    category_group = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='road_network')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='live')
    description    = models.TextField()
    features       = models.JSONField(default=list)
    order          = models.IntegerField(default=0)
    is_active      = models.BooleanField(default=True)
    created_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category_group', 'order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        name = 'san_pham_detail' if self.kind == 'product' else 'giai_phap_detail'
        return reverse(name, args=[self.key])


class NewsArticle(models.Model):
    slug         = models.SlugField(unique=True)
    title        = models.CharField(max_length=200)
    date         = models.DateField()
    author       = models.CharField(max_length=100)
    image_url    = models.URLField(max_length=500)
    summary      = models.TextField(max_length=300)
    content      = models.TextField()
    is_published = models.BooleanField(default=True)
    created_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class Project(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    image_url   = models.URLField(max_length=500)
    tags        = models.CharField(max_length=200)
    order       = models.IntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    quote       = models.TextField()
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=200)
    order       = models.IntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.author_name


class Partner(models.Model):
    name       = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=50, default='fa-building')
    order      = models.IntegerField(default=0)
    is_active  = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Stat(models.Model):
    label        = models.CharField(max_length=200)
    target_value = models.IntegerField()
    suffix       = models.CharField(max_length=20, default='+')
    icon         = models.CharField(max_length=50, default='fa-star')
    order        = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label
