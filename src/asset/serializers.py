import math
from rest_framework import serializers
from .models import Asset, Exchange
from django.utils import timezone
from datetime import timedelta

class ExchangeSerializer(serializers.ModelSerializer):
    last_updated = serializers.SerializerMethodField()
    class Meta:
        model = Exchange
        fields = ['name', 'url', 'image', 'daily_volume', 'last_updated']
    
    def get_last_updated(self,obj):
        # Calculate the time difference
        now = timezone.now()
        time_difference = now - obj.last_update

        # Format the time difference
        if time_difference < timedelta(minutes=5):
            return "recently"
        elif time_difference < timedelta(hours=1):
            minutes = time_difference.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif time_difference < timedelta(days=1):
            hours = time_difference.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = time_difference.days
            return f"{days} day{'s' if days != 1 else ''} ago"

class AssetSerializer(serializers.ModelSerializer):
    market = serializers.SerializerMethodField()
    _price = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['id', 'name', 'symbol', 'icon', 'rank', '_price', 'daily_change', 'market', 
                  'users_interested',]
    
    def get_market(self,obj):
        return "{:,}".format(obj.market_cap)
    def get__price(self,obj):
        return "{:,}".format(obj.price)

class AssetDetailSerializer(serializers.ModelSerializer):
    d_change = serializers.SerializerMethodField()
    market = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()
    diluted_valuation = serializers.SerializerMethodField()
    c_supply = serializers.SerializerMethodField()
    _price = serializers.SerializerMethodField()
    exchanges = ExchangeSerializer(many=True, read_only=True)
    update = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = ['id', 'name', 'symbol', 'rank', 'icon', '_price', 'price', 'd_change', 'market', 'volume', 'updated_at',
                  'users_interested', 'twitter', 'exchanges', 'update', 'description','diluted_valuation',
                  'high_24h','low_24h','price_change_percentage_24h','c_supply','ath',
                  'ath_change_percentage','ath_date','atl', 'atl_change_percentage', 'atl_date']


    def get_update(self,obj):
        # Calculate the time difference
        now = timezone.now()
        time_difference = now - obj.updated_at

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

    def get_d_change(self,obj):
        return "{:,}".format(obj.daily_change)
    
    def get_market(self,obj):
        return "{:,}".format(obj.market_cap)
    
    def get_volume(self,obj):
        return "{:,}".format(obj.total_volume)
    
    def get_diluted_valuation(self,obj):
        return "{:,}".format(obj.fully_diluted_valuation)
    
    def get_c_supply(self,obj):
        return "{:,}".format(obj.circulating_supply)
    
    def get__price(self,obj):
        return "{:,}".format(obj.price)
    
class AssetNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name']

class AssetFavSerializer(serializers.Serializer):
    asset_id = serializers.CharField()
    user_id = serializers.CharField()

class ExchangeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = "__all__"