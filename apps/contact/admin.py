from django.contrib import admin
from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'phone', 'organization', 'product_interest', 'created_at')
    list_filter   = ('product_interest',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
