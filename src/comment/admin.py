from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'content', 'news', 'created_at']

    @admin.display(description='user')
    def user_name(self, obj):
        return obj.user.username