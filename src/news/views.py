from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ListNewsSerializer, NewsLikeSerializer, NewsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework import generics
from .models import News
from account.models import User
from .tasks import news_update
import math
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

    def get_queryset(self):
        queryset = News.objects.all().filter(status='published')
        
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
        news = News.objects.all().filter(status='published')
        return Response({'size': math.ceil(news.count()/page_size)}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk:str):
        news = News.objects.get(id=pk)
        if not news:
            return Response({'error': 'Invalid Data'}, status=status.HTTP_403_FORBIDDEN)
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
        counter = 0
        for news in news_update():
            tags = news['tags']
            del news['tags']
            try:
                News.objects.get(title=news['title'])
            except:
                new_news = News.objects.create(**news)
                new_news.save()
                counter += 1

        return Response({'message':f'{counter} news added'}, status=status.HTTP_200_OK)