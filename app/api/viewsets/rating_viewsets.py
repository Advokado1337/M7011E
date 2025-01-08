from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token



from app.models import Movie,Rating
from app.api.serializers.movie_serializer import  RatingSerializer

from app.decorators import token_and_user_required, token_and_isstaff_required


class RatingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Ratings.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    @token_and_user_required
    def destroy(self, request, pk=None):

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Token required'}, status=401)

        token_key = auth_header.split('Token ')[1]
        user_id = Token.objects.get(key=token_key).user_id
        
        if pk is None:
            return Response({'error': 'Rating ID is required'}, status=400)
        try:
            rating = Rating.objects.get(pk=pk)
            if rating.user_id == user_id:
                rating.delete()
                return Response({'message': 'Rating deleted!'}, status=200)
            else:
                return Response({'error': 'Wrong user'}, status=404)
        except Rating.DoesNotExist:
            return Response({'error': 'Rating not found'}, status=404)
        
    
    @token_and_user_required
    def create(self, request):
        request_data = request.data

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Token required'}, status=401)

        token_key = auth_header.split('Token ')[1]
        user_id = Token.objects.get(key=token_key).user_id

        if 'stars' not in request_data or 'movie' not in request_data:
            return Response({'error': 'Stars and movie are required'}, status=400)
        
        if 'stars' in request_data and (request_data['stars'] < 1 or request_data['stars'] > 5):
            return Response({'error': 'Stars must be between 1 and 5'}, status=400)

        if 'text' not in request_data:
            text = request_data['text'] = ''
        else:
            text = request_data['text']

        try:
            movie = Movie.objects.get(name=request_data['movie'])
            movie_id = movie.id
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)

        if Rating.objects.filter(user_id=user_id, movie_id=movie_id).exists():
            return Response({'error': 'Rating already exists'}, status=400)

        rating_data = {
            'movie': movie_id,
            'user': user_id,
            'stars': request_data['stars'],
            'text': text
        }
        
        rating_serializer = RatingSerializer(data=rating_data)
        if rating_serializer.is_valid():
            rating_serializer.save()
            return Response(rating_serializer.data, status=201)
        return Response(rating_serializer.errors, status=400)
    
    @token_and_isstaff_required
    def destroy(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Rating ID is required'}, status=400)
        try:
            rating = Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            return Response({'error': 'Rating not found'}, status=404)
        
        rating.delete()
        return Response({'message': 'Rating deleted!'}, status=200)
    
    @token_and_isstaff_required
    def update(self, request):
        return Response({'error': 'Method not allowed'}, status=405)