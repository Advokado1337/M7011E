from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from app.models import  Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating
from rest_framework.authtoken.models import Token
from app.api.serializer import UsersSerializer, CategorySerializer, MovieSerializer, MovieCategorySerializer, MovieDirectorSerializer, MovieDirectorAssignmentSerializer, DescriptionSerializer, RatingSerializer,UserRegistrationSerializer
from django.contrib.auth.models import User
# Users CRUD operations
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(email=serializer.data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        user.set_password(serializer.data['password'])
        user.save()
        return Response({'email': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(request.data['password']):
        if Token.objects.get(user=user):
            Token.objects.get(user=user).delete()  # Delete the token if it was already created
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'email': UsersSerializer(user).data})
    return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    if Token.objects.filter(key=request.data['token']).exists():
        Token.objects.get(key=request.data['token']).delete()
        return Response({'message': 'Logout successful!'})
    return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        if request.method == 'PUT':
            serializer = UsersSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# Category CRUD operations
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            response_data = {
                'message': 'Category created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Movie CRUD operations
@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            response_data = {
                'message': 'Movie created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# MovieCategory CRUD operations
@api_view(['GET', 'POST'])
def movie_category_list(request):
    if request.method == 'GET':
        movie_categories = MovieCategory.objects.all()
        serializer = MovieCategorySerializer(movie_categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieCategorySerializer(data=request.data)
        if serializer.is_valid():
            movie_category = serializer.save()
            response_data = {
                'message': 'Movie category created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_category_detail(request, pk):
    try:
        movie_category = MovieCategory.objects.get(pk=pk)
    except MovieCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieCategorySerializer(movie_category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieCategorySerializer(movie_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# MovieDirector CRUD operations
@api_view(['GET', 'POST'])
def movie_director_list(request):
    if request.method == 'GET':
        movie_directors = MovieDirector.objects.all()
        serializer = MovieDirectorSerializer(movie_directors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieDirectorSerializer(data=request.data)
        if serializer.is_valid():
            movie_director = serializer.save()
            response_data = {
                'message': 'Movie director created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_director_detail(request, pk):
    try:
        movie_director = MovieDirector.objects.get(pk=pk)
    except MovieDirector.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieDirectorSerializer(movie_director)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieDirectorSerializer(movie_director, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie_director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# MovieDirectorAssignment CRUD operations
@api_view(['GET', 'POST'])
def movie_director_assignment_list(request):
    if request.method == 'GET':
        movie_director_assignments = MovieDirectorAssignment.objects.all()
        serializer = MovieDirectorAssignmentSerializer(movie_director_assignments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieDirectorAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            movie_director_assignment = serializer.save()
            response_data = {
                'message': 'Movie director assignment created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_director_assignment_detail(request, pk):
    try:
        movie_director_assignment = MovieDirectorAssignment.objects.get(pk=pk)
    except MovieDirectorAssignment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieDirectorAssignmentSerializer(movie_director_assignment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieDirectorAssignmentSerializer(movie_director_assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie_director_assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Description CRUD operations
@api_view(['GET', 'POST'])
def description_list(request):
    if request.method == 'GET':
        descriptions = Description.objects.all()
        serializer = DescriptionSerializer(descriptions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DescriptionSerializer(data=request.data)
        if serializer.is_valid():
            description = serializer.save()
            response_data = {
                'message': 'Description created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def description_detail(request, pk):
    try:
        description = Description.objects.get(pk=pk)
    except Description.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DescriptionSerializer(description)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DescriptionSerializer(description, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        description.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Rating CRUD operations
@api_view(['GET', 'POST'])
def rating_list(request):
    if request.method == 'GET':
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.save()
            response_data = {
                'message': 'Rating created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def rating_detail(request, pk):
    try:
        rating = Rating.objects.get(pk=pk)
    except Rating.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingSerializer(rating)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


