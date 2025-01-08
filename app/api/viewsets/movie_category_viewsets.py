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
    def update(self, request, pk=None):
        return Response({'error': 'Method not allowed'}, status=405)