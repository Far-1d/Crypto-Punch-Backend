from django.contrib import admin
from .models import Asset, Exchange
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Asset)
class AdminAsset(ModelAdmin):
     list_display = ['id', 'symbol', 'name', 'price', 'updated_at', 'rank', 'daily_change']

@admin.register(Exchange)
class AdminExchange(ModelAdmin):
     list_display = ['id', 'name', 'url', 'image', 'daily_volume', 'last_update']