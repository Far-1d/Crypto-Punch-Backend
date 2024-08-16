from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view()),

    # path('', views.NewsViewSet.as_view({
    #     'get': 'list'
    # })),
    path('pages/<int:page_size>', views.NewsViewSet.as_view({
        'get': 'number_pages'
    })),
    path('get/<str:pk>', views.NewsViewSet.as_view({
        'get': 'retrieve'
    })),
    path('like', views.NewsViewSet.as_view({
        'post': 'like'
    })),
    path('update', views.NewsViewSet.as_view({
        'get': 'update'
    })),
]