from datetime import timedelta
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from .serializers import AssetSerializer, AssetFavSerializer, AssetDetailSerializer, ExchangeListSerializer
from .models import Asset, Exchange
from account.models import User
import math
import random
from django.utils import timezone

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allow users to set the page size
    max_page_size = 200  # Set a maximum limit for page size

class CoinListView(generics.ListAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter,)
    search_fields = ['name', 'symbol']
    
    def get_queryset(self):
        queryset = Asset.objects.defer(
            'fully_diluted_valuation','circulating_supply','ath','ath_change_percentage','ath_date',
            'atl','atl_change_percentage','atl_date','price_change_percentage_24h', 'twitter', 'exchanges',
            'high_24h', 'low_24h', 'description'
        ).prefetch_related('users_interested').all()
        return queryset
 

# Create your views here.
class CoinViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk:str):
        if not is_positive_integer(pk):
            return Response({'error': 'Invalid Key'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            asset = Asset.objects.get(id=pk)
        except:
            return Response({'error': 'Invalid Key'}, status=status.HTTP_403_FORBIDDEN)
        list = AssetDetailSerializer(asset)
        return Response(list.data, status=status.HTTP_200_OK)

    def number_pages(self, request, page_size):
        if page_size == 0:
            return Response({'message': 'zero is not accepted'}, status=status.HTTP_400_BAD_REQUEST) 
        asset = Asset.objects.count()
        return Response({'size': math.ceil(asset/page_size)}, status=status.HTTP_200_OK)
    
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
        # counter = 0
        # updates = 0
        # for asset in get_coinList_with_marketData():
        #     _, created = Asset.objects.update_or_create(
        #         name=asset['name'],
        #         defaults=asset
        #     )
        #     if created:
        #         counter +=1
        #     else:
        #         updates += 1
        asset = Asset.objects.first()
        update = get_update(asset.updated_at)
        return Response({'message':f'Last update was {update}'}, status=status.HTTP_200_OK)

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
        # counter = 0
        # updates = 0
        # for exchange in get_exchange_date():
        #     _, created = Exchange.objects.update_or_create(
        #         name=exchange['name'],
        #         defaults=exchange
        #     )
        #     if created:
        #         counter +=1
        #     else:
        #         updates += 1
        exchange = Exchange.objects.first()
        update = get_update(exchange.updated_at)
        return Response({'message':f'Last update was {update}'}, status=status.HTTP_200_OK)

    def random(self, request, x:int):
        top_exchanges = Exchange.objects.all()[:20]
        exchanges = random.sample(list(top_exchanges), k=x)
        ser = ExchangeListSerializer(exchanges, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


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