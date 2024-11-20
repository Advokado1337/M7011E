"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.api.viewsets import users_list, users_detail, category_list, category_detail, movie_list, movie_detail, movie_category_list, movie_category_detail, movie_director_list, movie_director_detail, movie_director_assignment_list, movie_director_assignment_detail, description_list, description_detail, rating_list, rating_detail

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('/api/', include('app.api')),
    path('users/', users_list, name='users_list'),
    path('users/<int:pk>/', users_detail, name='users_detail'),
    path('categories/', category_list, name='category_list'),
    path('categories/<int:pk>/', category_detail, name='category_detail'),
    path('movies/', movie_list, name='movie_list'),
    path('movies/<int:pk>/', movie_detail, name='movie_detail'),
    path('movie-categories/', movie_category_list, name='movie_category_list'),
    path('movie-categories/<int:pk>/', movie_category_detail, name='movie_category_detail'),
    path('directors/', movie_director_list, name='movie_director_list'),
    path('directors/<int:pk>/', movie_director_detail, name='movie_director_detail'),
    path('director-assignments/', movie_director_assignment_list, name='movie_director_assignment_list'),
    path('director-assignments/<int:pk>/', movie_director_assignment_detail, name='movie_director_assignment_detail'),
    path('descriptions/', description_list, name='description_list'),
    path('descriptions/<int:pk>/', description_detail, name='description_detail'),
    path('ratings/', rating_list, name='rating_list'),
    path('ratings/<int:pk>/', rating_detail, name='rating_detail'),
]
