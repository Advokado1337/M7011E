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

# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'movies', MovieViewSet, basename='movies')
router.register(r'movie-categories', MovieCategoryViewSet, basename='movie-categories')
router.register(r'movie-directors', MovieDirectorViewSet, basename='movie-directors')
router.register(r'movie-director-assignments', MovieDirectorAssignmentViewSet, basename='movie-director-assignments')
router.register(r'descriptions', DescriptionViewSet, basename='descriptions')
router.register(r'ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # Register the API routes with versioning
]
