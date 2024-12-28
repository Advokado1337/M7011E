from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import action
from app.models import Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating
from app.api.serializer import (
    UsersSerializer, CategorySerializer, MovieSerializer, MovieCategorySerializer,
    MovieDirectorSerializer, MovieDirectorAssignmentSerializer, DescriptionSerializer,
    RatingSerializer, UserRegistrationSerializer
)
from app.decorators import token_and_superuser_required, token_and_staff_required

class UsersViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Users.
    """
    @action(detail=False, methods=['get'])
    @token_and_superuser_required
    def get_user(self, request):
        if 'pk' not in request.data:
            return Response({'error': 'User ID is required'}, status=400)
        try:
            user = User.objects.get(pk=request.data['pk'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        return Response(UsersSerializer(user).data, status=200)

    @action(detail=False, methods=['get'])
    @token_and_superuser_required
    def get_all_users(self, request):
        users = User.objects.all()
        return Response(UsersSerializer(users, many=True).data)

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
    
    @action(detail=False, methods=['delete'])
    @token_and_superuser_required
    def clear_token(self, request):
        Token.objects.all().delete()
        return Response({'message': 'Tokens cleared!'}, status=200)



class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Categories.
    """
    
    @action(detail=False, methods=['get'])
    def get_all_categories(self, request):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)

    @action(detail=False, methods=['get'])
    def get_category(self, request):
        if 'pk' not in request.data:
            return Response({'error': 'Category ID is required'}, status=400)
        try:
            category = Category.objects.get(pk=request.data['pk'])
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        return Response(CategorySerializer(category).data, status=200)
    
    @action(detail=False, methods=['post'])
    @token_and_staff_required
    def add_category(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @action(detail=False, methods=['delete'])
    @token_and_superuser_required
    def delete_category(self, request):
        if 'pk' not in request.data:
            return Response({'error': 'Category ID is required'}, status=400)
        try:
            category = Category.objects.get(pk=request.data['pk'])
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        
        # Delete all instances of the category in MovieCategory
        MovieCategory.objects.filter(category=category).delete()
        
        # Delete the category itself
        category.delete()
        return Response({'message': 'Category and related movie categories deleted!'}, status=200)


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
