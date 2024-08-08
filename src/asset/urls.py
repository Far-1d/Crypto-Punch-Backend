from django.urls import path
from . import views

app_name = 'asset'

urlpatterns = [
    path('update/', views.CoinViewSet.as_view({
        'get':'update'
    })),
    path('list/', views.CoinViewSet.as_view({
        'get':'list'
    })),
    path('add_favorite/', views.CoinViewSet.as_view({
        'post':'add_fav'
    })),
]