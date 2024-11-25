from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.viewsets import (
    UsersViewSet,
    CategoryViewSet,
    MovieViewSet,
    MovieCategoryViewSet,
    MovieDirectorViewSet,
    MovieDirectorAssignmentViewSet,
    DescriptionViewSet,
    RatingViewSet,
)

# Initialize the DefaultRouter for v1
router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'movies', MovieViewSet, basename='movies')
router_v1.register(r'movie-categories', MovieCategoryViewSet, basename='movie-categories')
router_v1.register(r'movie-directors', MovieDirectorViewSet, basename='movie-directors')
router_v1.register(r'movie-director-assignments', MovieDirectorAssignmentViewSet, basename='movie-director-assignments')
router_v1.register(r'descriptions', DescriptionViewSet, basename='descriptions')
router_v1.register(r'ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router_v1.urls)),  # Version 1
]