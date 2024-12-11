from rest_framework import serializers
from ..models import Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

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