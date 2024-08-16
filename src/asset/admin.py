from django.contrib import admin
from .models import Asset, Exchange

# Register your models here.
@admin.register(Asset)
class AdminAsset(admin.ModelAdmin):
     list_display = ['id', 'symbol', 'name', 'price', 'icon', 'rank', 'daily_change']

@admin.register(Exchange)
class AdminExchange(admin.ModelAdmin):
     list_display = ['id', 'name', 'url', 'image', 'daily_volume', 'last_update']