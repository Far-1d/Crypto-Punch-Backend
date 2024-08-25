from datetime import timedelta
from rest_framework import serializers
from .models import News, Category
from account.serializers import UserSerializer
from asset.serializers import AssetNameSerializer
from django.utils import timezone

class NewsSerializer(serializers.ModelSerializer):
    tags = AssetNameSerializer(many=True, read_only=True)
    writer = UserSerializer(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'tags', 'likes', 'writer', 'published_at', 'updated_at']
    
class ListNewsSerializer(NewsSerializer):
    # tags = AssetNameSerializer(many=True, read_only=True)
    tag_names = serializers.SerializerMethodField()
    writer = UserSerializer(read_only=True)
    # content_short = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    publish = serializers.SerializerMethodField()
    # tag_names = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'tag_names', 'likes_count', 'writer', 'published_at', 'publish']
    
    # def get_content_short(self, obj):
    #     return obj.content[:100]   
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_publish(self,obj):
        # Calculate the time difference
        now = timezone.now()
        time_difference = now - obj.published_at

        # Format the time difference
        if time_difference < timedelta(minutes=5):
            return "recently"
        elif time_difference < timedelta(hours=1):
            minutes = time_difference.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif time_difference < timedelta(days=1):
            hours = time_difference.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = time_difference.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        
class NewsLikeSerializer(serializers.Serializer):

    news_id = serializers.CharField()
    user_id = serializers.CharField()
