from django.contrib import admin
from .models import Product, NewsArticle, Project, Testimonial, Partner, Stat


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category_group', 'status', 'order', 'is_active')
    list_filter   = ('category_group', 'status', 'is_active')
    search_fields = ('title', 'key')
    ordering      = ('category_group', 'order')


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display  = ('title', 'date', 'author', 'is_published')
    list_filter   = ('is_published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'order', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('title',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'order', 'is_active')
    list_filter  = ('is_active',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'order', 'is_active')
    list_filter  = ('is_active',)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('label', 'target_value', 'suffix', 'order')
