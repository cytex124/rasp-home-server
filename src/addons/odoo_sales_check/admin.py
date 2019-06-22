from django.contrib import admin
from .models import AuditSalesCheck, OdooProduct, RepoMaintainer


@admin.register(RepoMaintainer)
class RepoMaintainerAdmin(admin.ModelAdmin):
    list_display = ['repo_id', 'name']


@admin.register(OdooProduct)
class OdooProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'repo']


@admin.register(AuditSalesCheck)
class AuditSalesCheckAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'amount', 'created_at']
