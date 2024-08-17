from django.contrib import admin
from .models import News, Category
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(News)
class AdminNews(ModelAdmin):
    list_display = ['id', 'title_short', 'content_short', 'writer_name', 'likes_count', 'category', 'status', 'published_at']
    list_filter = ["status", 'category', "published_at"]
    search_fields = ['title', 'content']

    @admin.display(description='title')
    def title_short(self, obj):
        return obj.title[:50] + "..." if len(obj.title)>52 else ""
    
    @admin.display(description='content')
    def content_short(self, obj):
        return obj.content[:100]+"..." if len(obj.content)>102 else ""
    
    @admin.display(description='Writer')
    def writer_name(self, obj):
        return obj.writer.username if obj.writer else "Unknown"
    
    @admin.display(description='Likes Count')
    def likes_count(self, obj):
        return obj.likes.count()
    
@admin.register(Category)
class AdminNews(ModelAdmin):
    list_display = ['id', 'name', 'description']