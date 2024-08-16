from rest_framework import serializers
from .models import News, Category
from account.serializers import UserSerializer
from asset.serializers import AssetNameSerializer

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
    # tag_names = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'tag_names', 'likes_count', 'writer', 'published_at']
    
    # def get_content_short(self, obj):
    #     return obj.content[:100]   
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
class NewsLikeSerializer(serializers.Serializer):

    news_id = serializers.CharField()
    user_id = serializers.CharField()
