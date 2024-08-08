from django.shortcuts import render
from rest_framework import viewsets
from .models import Asset

# Create your views here.
class CoinViewSet(viewsets.ViewSet):
    def update(self, request):
        pass

    def list(self, request):
        pass

    def add_fav(self, request):
        pass