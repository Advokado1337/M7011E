from django.contrib import admin
from django.urls import path, include
from app.api.viewsets import (
    users_list, users_detail, category_list, category_detail, movie_list, movie_detail,
    movie_category_list, movie_category_detail, movie_director_list, movie_director_detail,
    movie_director_assignment_list, movie_director_assignment_detail, description_list,
    description_detail, rating_list, rating_detail
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', users_list, name='users_list'),
    path('api/users/<int:pk>/', users_detail, name='users_detail'),
    path('api/categories/', category_list, name='category_list'),
    path('api/categories/<int:pk>/', category_detail, name='category_detail'),
    path('api/movies/', movie_list, name='movie_list'),
    path('api/movies/<int:pk>/', movie_detail, name='movie_detail'),
    path('api/movie-categories/', movie_category_list, name='movie_category_list'),
    path('api/movie-categories/<int:pk>/', movie_category_detail, name='movie_category_detail'),
    path('api/movie-directors/', movie_director_list, name='movie_director_list'),
    path('api/movie-directors/<int:pk>/', movie_director_detail, name='movie_director_detail'),
    path('api/movie-director-assignments/', movie_director_assignment_list, name='movie_director_assignment_list'),
    path('api/movie-director-assignments/<int:pk>/', movie_director_assignment_detail, name='movie_director_assignment_detail'),
    path('api/descriptions/', description_list, name='description_list'),
    path('api/descriptions/<int:pk>/', description_detail, name='description_detail'),
    path('api/ratings/', rating_list, name='rating_list'),
    path('api/ratings/<int:pk>/', rating_detail, name='rating_detail'),
]