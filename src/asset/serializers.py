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

    class Meta:
        model = Asset
        fields = ['id', 'name', 'symbol', 'icon', 'price', 'daily_change', 'market_cap', 
                  'users_interested',]
        
class AssetDetailSerializer(serializers.ModelSerializer):
    exchanges = ExchangeSerializer(many=True, read_only=True)
    created_at_formated = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = ['id', 'name', 'symbol', 'icon', 'price', 'daily_change', 'market_cap', 
                  'users_interested', 'twitter', 'exchanges', 'created_at_formated', 'description']
    
    def get_created_at_formated(self,obj):
        # Calculate the time difference
        now = timezone.now()
        time_difference = now - obj.created_at

        # Format the time difference
        if time_difference > timedelta(days=1):
            days = time_difference.days
            if days <30:
                return f"{days} day{'s' if days != 1 else ''} ago"
            elif 30 <= days <365 :
                months = math.floor(days/30)
                return f"over {'a' if months==1 else months} year{'s' if months != 1 else ''} ago"
            elif days >= 365:
                years = math.floor(days/365)
                return f"over {'a' if years==1 else years} year{'s' if years != 1 else ''} ago"
        else:
            return "today"


class AssetNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name']