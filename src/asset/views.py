from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from .serializers import AssetSerializer, AssetFavSerializer, AssetDetailSerializer, ExchangeListSerializer
from .models import Asset, Exchange
from .tasks import get_coinList_with_marketData, get_exchange_date
from account.models import User
import math

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allow users to set the page size
    max_page_size = 200  # Set a maximum limit for page size

class CoinListView(generics.ListAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter,)
    search_fields = ['name', 'symbol']

# Create your views here.
class CoinViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk:str):
        asset = Asset.objects.get(id=pk)
        if not asset:
            return Response({'error': 'Invalid Data'}, status=status.HTTP_403_FORBIDDEN)
        list = AssetDetailSerializer(asset)
        return Response(list.data, status=status.HTTP_200_OK)

    def number_pages(self, request, page_size):
        asset = Asset.objects.all()
        return Response({'size': math.ceil(asset.count()/page_size)}, status=status.HTTP_200_OK)
    
    def add_fav(self, request):
        data = AssetFavSerializer(data=request.data)
        if data.is_valid():
            asset_id = data.validated_data['asset_id']
            user_id = data.validated_data['user_id']
            try:
                asset = Asset.objects.get(id=asset_id)
                user = User.objects.get(id=user_id)

                if user in asset.users_interested.all():
                    asset.users_interested.remove(user)
                    return Response({'message': 'removed', 'count': asset.users_interested.count()}, status=status.HTTP_200_OK)
                else:
                    asset.users_interested.add(user)
                    return Response({'message': 'added', 'count': asset.users_interested.count()}, status=status.HTTP_200_OK)
            except Asset.DoesNotExist:
                return Response({'message': 'Asset not found.'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        counter = 0
        updates = 0
        for asset in get_coinList_with_marketData():
            _, created = Asset.objects.update_or_create(
                name=asset['name'],
                defaults=asset
            )
            if created:
                counter +=1
            else:
                updates += 1

        return Response({'message':f'{counter} assets added and {updates} assets updated'}, status=status.HTTP_200_OK)

    def is_fav(self, request):
        data = AssetFavSerializer(data=request.data)
        if data.is_valid():
            asset_id = data.validated_data['asset_id']
            user_id = data.validated_data['user_id']
            try:
                asset = Asset.objects.get(id=asset_id)
                user = User.objects.get(id=user_id)

                if user in asset.users_interested.all():
                    return Response({'message': 'yes', 'count': asset.users_interested.count()}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'no', 'count': asset.users_interested.count()}, status=status.HTTP_200_OK)
            except Asset.DoesNotExist:
                return Response({'message': 'Asset not found.'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExchangeSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def update(self, request):
        counter = 0
        updates = 0
        for exchange in get_exchange_date():
            _, created = Exchange.objects.update_or_create(
                name=exchange['name'],
                defaults=exchange
            )
            if created:
                counter +=1
            else:
                updates += 1

        return Response({'message':f'{counter} assets added and {updates} assets updated'}, status=status.HTTP_200_OK)

    def random(self, request, x:int):
        exchanges = Exchange.objects.order_by('?')[:x]
        ser = ExchangeListSerializer(exchanges, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
