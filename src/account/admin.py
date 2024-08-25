from django.contrib import admin
from .models import User
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(User)
class AdminUser(ModelAdmin):
     list_display = ['id', 'username', 'email', 'role', 'created', 'last_login']