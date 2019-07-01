from django.contrib import admin
from .models import Band, Proxy, Vote


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ['choice_id', 'name']


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ['url']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['created_at']
