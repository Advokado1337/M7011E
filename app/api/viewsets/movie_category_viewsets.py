from rest_framework import viewsets
from rest_framework.response import Response


from app.models import Category, Movie, MovieCategory
from app.api.serializers.movie_serializer import MovieCategorySerializer
from app.decorators import  token_and_isstaff_required


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