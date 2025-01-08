from rest_framework import viewsets
from rest_framework.response import Response


from app.models import MovieDirectorAssignment
from app.api.serializers.movie_serializer import ( MovieDirectorAssignmentSerializer, 
    
)
from app.decorators import  token_and_isstaff_required


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
