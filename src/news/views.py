from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ListNewsSerializer, NewsLikeSerializer, NewsSerializer, NewsCreateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework import generics
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from .models import News, Category
from account.models import User
from account.oauth import verify_token
import math
import os
# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allow users to set the page size
    max_page_size = 100  # Set a maximum limit for page size

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().filter(status='published')
    serializer_class = ListNewsSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter,)
    search_fields = ['title', 'content', 'tag_names__name']  # Fields to search on

    # start redis before cache 

    # @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = News.objects.defer('content').select_related('writer').prefetch_related('tags', 'likes').all().filter(status='published')
        
        # Filter by creation date if provided in query parameters
        created_after = self.request.query_params.get('created_after', None)
        created_before = self.request.query_params.get('created_before', None)

        if created_after:
            queryset = queryset.filter(updated_at__gte=created_after)
        if created_before:
            queryset = queryset.filter(updated_at__lte=created_before)

        return queryset
    
class NewsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        news = News.objects.all().filter(status='published')
        serialized_news = ListNewsSerializer(news, many=True)
        return Response(serialized_news.data, status=status.HTTP_200_OK)
    
    def number_pages(self, request, page_size):
        if page_size == 0:
           return Response({'message': 'zero is not accepted'}, status=status.HTTP_400_BAD_REQUEST) 
        news = News.objects.all().filter(status='published').count()
        return Response({'size': math.ceil(news/page_size)}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk:str):
        if not is_positive_integer(pk):
            return Response({'error': 'Invalid Key'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            news = News.objects.get(id=pk)
        except:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        list = NewsSerializer(news)
        return Response(list.data, status=status.HTTP_200_OK)
    
    def like(self, request):
        news_like = NewsLikeSerializer(data=request.data)
        if news_like.is_valid():
            news_id = news_like.validated_data['news_id']
            user_id = news_like.validated_data['user_id']
            try:
                news = News.objects.get(id=news_id)
                user = User.objects.get(id=user_id)

                if user in news.likes.all():
                    news.likes.remove(user)
                    return Response({'message': 'unliked'}, status=status.HTTP_200_OK)
                else:
                    news.likes.add(user)
                    return Response({'message': 'liked'}, status=status.HTTP_200_OK)
            except News.DoesNotExist:
                return Response({'message': 'News not found.'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(news_like.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request):
        news = News.objects.first()
        update = get_update(news.updated_at)
        return Response({'message':f'Latest news added {update}'}, status=status.HTTP_200_OK)
    
    def create(self, request):
        serialized_data = NewsCreateSerializer(data=request.data)
        if serialized_data.is_valid():
            news_item = serialized_data.save()
            return Response({'message':'success', 'data':serialized_data.data}, status=status.HTTP_201_CREATED)

        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


def is_positive_integer(user_input):
    try:
        value = int(user_input)
        return value > 0
    except:
        return False

def get_update(time):
        # Calculate the time difference
        now = timezone.now()
        time_difference = now -time

        # Format the time difference
        if time_difference < timedelta(minutes=1):
            return "Just now"
        elif time_difference < timedelta(hours=1):
            minutes = time_difference.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif time_difference < timedelta(days=1):
            hours = time_difference.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = time_difference.days
            return f"{days} day{'s' if days != 1 else ''} ago"