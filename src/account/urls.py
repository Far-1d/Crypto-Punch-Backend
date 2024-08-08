from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('get/<str:pk>', views.UserViewSet.as_view({
        'get':'get_user'
    })),
    path('signup', views.UserViewSet.as_view({
        'post':'signup'
    })),
    path('login', views.UserViewSet.as_view({
        'post':'login'
    })),
    path('update/<str:pk>', views.UserViewSet.as_view({
        'post':'update'
    })),
    path('delete/<str:pk>', views.UserViewSet.as_view({
        'get':'delete'
    })),
    path('list_favorite', views.UserViewSet.as_view({
        'get':'list_favorite'
    })),
    path('add_favorite', views.UserViewSet.as_view({
        'post':'add_favorite'
    }))
]