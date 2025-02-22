from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.decorators import action
from app.api.serializers.user_serializer import (
    UsersSerializer, UserRegistrationSerializer
)
from app.decorators import token_and_superuser_required
import requests
import jwt
from django.shortcuts import get_object_or_404
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from random import SystemRandom
from urllib.parse import urlencode
from config.settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET


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
    

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def google_login(self, request):
        # Create state token to prevent CSRF attacks
        state = self._generate_state_token()
        request.session["google_oauth2_state"] = state

        # Scope for the Google OAuth2 API
        client_id = GOOGLE_CLIENT_ID

        params = {
            'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
            'access_type': 'offline',
            'include_granted_scopes': 'true',
            'response_type': 'code',
            'state': state,
            'client_id': client_id,
            'redirect_uri': 'http://localhost:8000/api/v1/users/google_login_callback/'
        }

        query_params = urlencode(params)
        auth_url = f'https://accounts.google.com/o/oauth2/auth?{query_params}'

        return redirect(auth_url)

    @staticmethod
    def _generate_state_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        rand = SystemRandom()
        state_value = "".join(rand.choice(chars) for _ in range(length))
        return state_value

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def google_login_callback(self, request):
        data = request.GET

        code = data.get('code')
        error = data.get('error')
        state = data.get('state')

        # Handle possible errors/state codes
        if error is not None:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        if code is None or state is None:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        session_state = request.session.get("google_oauth2_state")
        if session_state is None or session_state != state:
            return Response({'error': 'Invalid state'}, status=status.HTTP_400_BAD_REQUEST)

        del request.session["google_oauth2_state"]

        # Decode the JWT access token and get user info
        tokens = self.get_tokens(code)
        user_info = self.get_user_info(tokens['access_token'])

        # Check if user already exists in the database
        try:
            user = User.objects.get(email=user_info['email'])
        except User.DoesNotExist:
            user = User.objects.create_user(email=user_info['email'], username=user_info['name'].replace(' ', ''))
            user.save()

        # Create a new auth token for the user
        Token.objects.filter(user=user).delete()  # Remove old token
        token = Token.objects.create(user=user)

        # Return the token and user info
        return Response({'state': session_state, 'token': token.key, 'user data': UsersSerializer(user).data}, status=200)

    def get_tokens(self, code: str):
        data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8000/api/v1/users/google_login_callback/',
            'grant_type': 'authorization_code'
        }

        response = requests.post('https://accounts.google.com/o/oauth2/token', data=data)
        google_tokens = response.json()

        return google_tokens

    def get_user_info(self, access_token: str):
        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers={'Authorization': f'Bearer {access_token}'})
        user_info = response.json()

        return user_info