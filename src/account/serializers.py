import math
from rest_framework import serializers
from .models import User
from django.utils import timezone
from datetime import timedelta

class UserSerializer(serializers.ModelSerializer):
    last_login_formatted = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at', 'image', 'last_login_formatted']

    def get_last_login_formatted(self, obj):
        if obj.last_login is None:
            return "Never logged in"

        # Calculate the time difference
        now = timezone.now()
        time_difference = now - obj.last_login

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
    
    def get_created_at(self, obj):
        # Calculate the time difference
        now = timezone.now()
        time_difference = now - obj.created

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

class SignupSerializer(serializers.ModelSerializer): # modelSerializer is ok for create and update
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user

class LoginSerializer(serializers.Serializer): #serializer will not check for uniqueness 
    username = serializers.CharField()
    password = serializers.CharField()

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    secret = serializers.CharField()
    
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
