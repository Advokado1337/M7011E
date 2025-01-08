from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction


from app.models import Category, Movie, MovieCategory, Description
from app.api.serializers.movie_serializer import ( MovieSerializer, DescriptionSerializer
    
)
from app.decorators import token_and_superuser_required, token_and_isstaff_required



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





