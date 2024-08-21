from django.urls import path
from . import views

app_name = 'asset'

urlpatterns = [
    path('list', views.CoinListView.as_view()),
    path('get/<str:pk>', views.CoinViewSet.as_view({
        'get':'get'
    })),
    path('pages/<int:page_size>', views.CoinViewSet.as_view({
        'get': 'number_pages'
    })),
    path('update', views.CoinViewSet.as_view({
        'get':'update'
    })),
    path('favorite', views.CoinViewSet.as_view({
        'post':'add_fav'
    })),
    path('isFavorite', views.CoinViewSet.as_view({
        'post':'is_fav'
    })),

    path('update_exchange', views.ExchangeSet.as_view({
        'get':'update'
    })),
    path('random_exchange/<int:x>', views.ExchangeSet.as_view({
        'get':'random'
    })),
]