from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.decorators import action
from app.models import Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating
from app.api.serializer import (
    UsersSerializer, CategorySerializer, MovieSerializer, MovieCategorySerializer,
    MovieDirectorSerializer, MovieDirectorAssignmentSerializer, DescriptionSerializer,
    RatingSerializer, UserRegistrationSerializer
)
from app.decorators import token_and_superuser_required
import requests
import jwt
from config.settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

class UsersViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Users.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
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
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Token required'}, status=401)

        token_key = auth_header.split('Token ')[1]
        Token.objects.filter(key=token_key).delete()
        return Response({'message': 'Logout successful!'}, status=200)

    @action(detail=False, methods=['put'])
    @token_and_superuser_required
    def update_role(self, request):
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        user.is_staff = request.data['is_staff']
        user.save()
        return Response({'email': UsersSerializer(user).data})
    
    # TODO: Implement the Google OAuth2 login in a separate class
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def google_login(self, request):
        # Create state token to prevent CSRF attacks
        # TODO: Generate a secure state token using SystemRandom and UNICODE ASCII characters
        state = '123'
        request.session["google_oauth2_state"] = state

        # Scope for the Google OAuth2 API
        # TODO: Clean up the code (use urlencode, make params dict and use string formatting)
        client_id = GOOGLE_CLIENT_ID
        auth_url = ('https://accounts.google.com/o/oauth2/auth?'
                    'scope=https%3A//www.googleapis.com/auth/userinfo.email%20https%3A//www.googleapis.com/auth/userinfo.profile&'
                    'access_type=offline&'
                    'include_granted_scopes=true&'
                    'response_type=code&'
                    'state={}&'
                    'client_id={}&'
                    'redirect_uri=http://localhost:8000/api/v1/users/google_login_callback/'.format(state, client_id))
        
        return redirect(auth_url)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def google_login_callback(self, request):

        # TODO: Create a serializer for the data
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

        # Decode the JWT id_token

        tokens = self.get_tokens(code)
        id_token_decoded = jwt.decode(jwt=tokens['id_token'], options={'verify_signature': False})

        # Check if user already exists in the database
            # If user exists, log the user in and return the auth token

        user_email = id_token_decoded['email']

        # If user does not exist, create a new user

        # Create a new auth token for the user

        # Return the token and user info
        return Response({'user email': user_email}, status=200)
    
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

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieCategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movie Categories.
    """
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer


class MovieDirectorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movie Directors.
    """
    queryset = MovieDirector.objects.all()
    serializer_class = MovieDirectorSerializer


class MovieDirectorAssignmentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movie Director Assignments.
    """
    queryset = MovieDirectorAssignment.objects.all()
    serializer_class = MovieDirectorAssignmentSerializer


class DescriptionViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Descriptions.
    """
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Ratings.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
