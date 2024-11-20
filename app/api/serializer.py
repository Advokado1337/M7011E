from rest_framework import serializers
from ..models import Users, Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'username', 'password']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name']

class MovieCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCategory
        fields = ['id', 'movie', 'category']

class MovieDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDirector
        fields = ['id', 'firstname', 'surname']

class MovieDirectorAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDirectorAssignment
        fields = ['id', 'movie', 'director']

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'movie', 'description']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'movie', 'user', 'stars', 'text']