import time
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import User
from .serializers import LoginSerializer, SignupSerializer, TokenSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.utils import timezone
from .oauth import create_token, verify_token
# from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

# Create your views here.
class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        user = serializer.save()

        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        user_serializer = UserSerializer(user)
        return Response(create_token(user_serializer.data), status=status.HTTP_201_CREATED)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            user_serializer = UserSerializer(user)
            return Response(create_token(user_serializer.data), status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get_user(self, request, pk:str):
        user = User.objects.get(id=pk)
        if not user:
            return Response({'error': 'Invalid Data'}, status=status.HTTP_403_FORBIDDEN)

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def list_favorite(self, request):
        pass

    def update(self, request):
        pass

    def delete(self, request):
        pass
    
    def get_queryset(self):
        return User.objects.all()