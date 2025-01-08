from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import action

from app.api.serializers.user_serializer import (
    UsersSerializer, UserRegistrationSerializer
)
from app.decorators import token_and_superuser_required

class UsersViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Users.

    """

    @token_and_superuser_required
    def list(self, request):
        """
        Retrieve a list of all users.
        """
        queryset = User.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)

    @token_and_superuser_required
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific user by ID.
        """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        """
        Register a new user.
        """
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'error': 'Email and password are required'}, status=400)
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 'Email already exists'}, status=400)
            user = serializer.create(serializer.validated_data)
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'email': serializer.data}, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Log in a user and return an authentication token.
        """
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'error': 'Email and password are required'}, status=400)
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if user.check_password(request.data['password']):
            Token.objects.filter(user=user).delete()  # Remove old token
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'email': UsersSerializer(user).data}, status=200)
        return Response({'error': 'Invalid password'}, status=400)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Log out the current user by deleting their authentication token.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Token required'}, status=401)

        token_key = auth_header.split('Token ')[1]
        Token.objects.filter(key=token_key).delete()
        return Response({'message': 'Logout successful!'}, status=200)

    @action(detail=False, methods=['put'])
    @token_and_superuser_required
    def update_role(self, request):
        """
        Update the role of a user.
        """
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        user.is_staff = request.data['is_staff']
        user.save()
        return Response({'email': UsersSerializer(user).data})
    
    @action(detail=False, methods=['delete'])
    @token_and_superuser_required
    def clear_token(self, request):
        """
        Clear all authentication tokens.
        """
        Token.objects.all().delete()
        return Response({'message': 'Tokens cleared!'}, status=200)