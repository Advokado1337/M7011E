from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction


from app.models import MovieDirector, MovieDirectorAssignment
from app.api.serializers.movie_serializer import MovieDirectorSerializer
    
from app.decorators import token_and_superuser_required, token_and_isstaff_required



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