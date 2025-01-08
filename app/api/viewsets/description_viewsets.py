from rest_framework import viewsets
from rest_framework.response import Response



from app.models import  Description
from app.api.serializers.movie_serializer import ( DescriptionSerializer,
    
)
from app.decorators import token_and_isstaff_required


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