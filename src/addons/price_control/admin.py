from django.contrib import admin
from .models import PriceControlPage, AuditControl, ProductPriceControl


@admin.register(PriceControlPage)
class PriceControlPageAdmin(admin.ModelAdmin):
    list_display = ['web_page', 'suffix_url', 'product']


@admin.register(AuditControl)
class AuditControlAdmin(admin.ModelAdmin):
    list_display = ['price', 'price_control_page', 'created_at']


@admin.register(ProductPriceControl)
class ProductPriceControlAdmin(admin.ModelAdmin):
    list_display = ['name', 'wish_price', 'currency']
