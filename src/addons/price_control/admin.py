from django.contrib import admin
from .models import Page, AuditLog, Product


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['web_page', 'suffix_url', 'product']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['price', 'page', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'wish_price', 'currency']
