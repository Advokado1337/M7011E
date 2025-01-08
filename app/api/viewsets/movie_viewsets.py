from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction


from app.models import Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating
from app.api.serializers.movie_serializer import (
     CategorySerializer, MovieSerializer, MovieCategorySerializer,
    MovieDirectorSerializer, MovieDirectorAssignmentSerializer, DescriptionSerializer,
    RatingSerializer
)
from app.decorators import token_and_superuser_required, token_and_isstaff_required




class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Categories.
    """
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @token_and_isstaff_required
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new category.
        """
        category_data = request.data

        if 'category' not in category_data:
            return Response({'error': 'Category is required'}, status=400)

        if 'category' in category_data and Category.objects.filter(category=category_data['category']).exists():
            return Response({'error': 'Category already exists'}, status=400)

        category_serializer = CategorySerializer(data={'category': category_data['category']})
        if category_serializer.is_valid():
            category_serializer.save()  # Save category instance
        else:
            return Response(category_serializer.errors, status=400)

        return Response(category_serializer.data, status=201)

    @token_and_superuser_required
    def destroy(self, request, pk=None):
        """
        Delete a category by ID.
        """
        if pk is None:
            return Response({'error': 'Category ID is required'}, status=400)
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)

        MovieCategory.objects.filter(category=category).delete()
        category.delete()
        return Response({'message': 'Category deleted!'}, status=200)

class MovieViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @token_and_isstaff_required
    @transaction.atomic  
    #@transaction.atomic decorator in Django is used to wrap the execution of a function in a database transaction. 
    # This ensures that all the database operations within the function are executed as a single unit. 
    # If any operation within the transaction fails, the entire transaction is rolled back, ensuring the database remains in a consistent state.
    def create(self, request, *args, **kwargs):
        movie_data = request.data

        if 'name' not in movie_data or 'description' not in movie_data or 'category' not in movie_data or '':
            return Response({'error': 'Name, description, and category are required'}, status=400)
        
        if 'name' in movie_data and Movie.objects.filter(name=movie_data['name']).exists():
            return Response({'error': 'Movie already exists'}, status=400)

        name_data = movie_data['name']
        category_data = movie_data['category']
        description_text = movie_data['description']

        movie_serializer = MovieSerializer(data={'name': name_data})
        if movie_serializer.is_valid():
            movie = movie_serializer.save()  # Save movie instance
        else:
            return Response(movie_serializer.errors, status=400)

        description_data = {
            'description': description_text,
            'movie': movie.id
        }
        description_serializer = DescriptionSerializer(data=description_data)
        if description_serializer.is_valid():
            description_serializer.save()
        else:
            movie.delete()
            return Response(description_serializer.errors, status=400)

        for category_name in category_data:
            try:
                category = Category.objects.get(category=category_name)
                MovieCategory.objects.create(movie=movie, category=category)
            except Category.DoesNotExist:
                Description.objects.filter(movie=movie).delete()
                movie.delete()
                return Response({'error': f'Category with Name {category_name} not found'}, status=404)
            
        return Response(movie_serializer.data, status=201)

    
    @token_and_superuser_required
    def destroy(self, request,pk=None):
        if pk is None:
            return Response({'error': 'Movie ID is required'}, status=400)
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)
        
        movie.delete()
        return Response({'message': 'Movie deleted!'}, status=200)
    
    @token_and_isstaff_required
    def update(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Movie ID is required'}, status=400)
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)
        
        if 'name' in request.data:
            movie.name = request.data['name']
        
        if 'description' in request.data:
            try:
                description = Description.objects.get(movie=movie)
                description.description = request.data['description']
                description.save()
            except Description.DoesNotExist:
                return Response({'error': 'Description not found'}, status=404)
        
        if 'category' in request.data:
            MovieCategory.objects.filter(movie=movie).delete()
            for category_name in request.data['category']:
                try:
                    category = Category.objects.get(category=category_name)
                    MovieCategory.objects.create(movie=movie, category=category)
                except Category.DoesNotExist:
                    return Response({'error': f'Category with name {category_name} not found'}, status=404)
        return Response(MovieSerializer(movie).data,status=200)

class MovieCategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movie Categories.
    """
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer
    
    @token_and_isstaff_required
    def destroy(self, request, pk=None):
        return Response({'error': 'Method not allowed'}, status=405)
    
    @token_and_isstaff_required
    def create(self, request):
        return Response({'error': 'Method not allowed'}, status=405)

    @token_and_isstaff_required
    def update(self, request):
        movie_data = request.data
        if not Movie.objects.filter(name=movie_data['movie']).exists():
            return Response({'error': 'Movie name is required'}, status=400)
        try:
            movie = Movie.objects.filter(name=movie_data['movie'])
            movie_category = MovieCategory.objects.get(movie_id=movie[0].id)
        except MovieCategory.DoesNotExist:
            return Response({'error': 'Movie Category not found'}, status=404)
        
        if 'category' in request.data:
            try:
                category = Category.objects.get(pk=movie_category.id)
                movie_category.category = request.data['category']
            except Category.DoesNotExist:
                return Response({'error': f'Category with ID {movie_category.idgory_id} not found'}, status=404)
        
        movie_category.save()
        return Response(MovieCategorySerializer(movie_category).data,status=204)

class MovieDirectorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movie Directors.
    """
    queryset = MovieDirector.objects.all()
    serializer_class = MovieDirectorSerializer

    @token_and_isstaff_required
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        director_data = request.data

        if 'firstname' not in director_data or 'surname' not in director_data:
            return Response({'error': 'Firstname and surname are required'}, status=400)

        if MovieDirector.objects.filter(firstname=director_data['firstname'], surname=director_data['surname']).exists():
            return Response({'error': 'Director already exists'}, status=400)

        director_serializer = MovieDirectorSerializer(data=director_data)
        if director_serializer.is_valid():
            director_serializer.save()  # Save director instance
        else:
            return Response(director_serializer.errors, status=400)

        return Response(director_serializer.data, status=201)

    @token_and_superuser_required
    def destroy(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Director ID is required'}, status=400)
        try:
            director = MovieDirector.objects.get(pk=pk)
        except MovieDirector.DoesNotExist:
            return Response({'error': 'Director not found'}, status=404)

        MovieDirectorAssignment.objects.filter(director_id=director).delete()
        director.delete()
        return Response({'message': 'Director deleted!'}, status=200)
    
    def update(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Director ID is required'}, status=400)
        try:
            director = MovieDirector.objects.get(pk=pk)
        except MovieDirector.DoesNotExist:
            return Response({'error': 'Director not found'}, status=404)
        
        if 'firstname' not in request.data and 'surname' not in request.data:
            return Response({'error': 'Firstname or Surname is required'}, status=400)

        if 'firstname' in request.data:
            director.firstname = request.data['firstname']  
        
        if 'surname' in request.data:
            director.surname = request.data['surname']
        
        
        director.save()
        return Response(MovieDirectorSerializer(director).data,status=204)

class MovieDirectorAssignmentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Movie Director Assignments.
    """
    queryset = MovieDirectorAssignment.objects.all()
    serializer_class = MovieDirectorAssignmentSerializer

    @token_and_isstaff_required
    def destroy(self, request, pk=None):
        return Response({'error': 'Method not allowed'}, status=405)
    
    @token_and_isstaff_required
    def update(self, request, pk=None):
        return Response({'error': 'Method not allowed'}, status=405)
    
    @token_and_isstaff_required
    def create(self, request):
        return Response({'error': 'Method not allowed'}, status=405)

class DescriptionViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Descriptions.
    """
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    
    @token_and_isstaff_required
    def update(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Description ID is required'}, status=400)
        try:
            description = Description.objects.get(pk=pk)
        except Description.DoesNotExist:
            return Response({'error': 'Description not found'}, status=404)
        
        if 'description' in request.data:
            description.description = request.data['description']
            description.save()
        else:
            return Response({'error': 'Description is required'}, status=400)
        
        return Response(DescriptionSerializer(description).data,status=204)
    
    @token_and_isstaff_required
    def destroy(self, request, pk=None):
        return Response({'error': 'Method not allowed'}, status=405)
    
    @token_and_isstaff_required
    def create(self, request):
        return Response({'error': 'Method not allowed'}, status=405)

class RatingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Ratings.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
