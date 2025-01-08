from django.contrib import admin
from django.urls import path, include,re_path

from rest_framework.routers import DefaultRouter
from app.api.viewsets.movie_viewsets import   MovieViewSet
from app.api.viewsets.user_viewsets import UsersViewSet
from app.api.viewsets.category_viewsets import CategoryViewSet
from app.api.viewsets.description_viewsets import DescriptionViewSet
from app.api.viewsets.movie_category_viewsets import MovieCategoryViewSet
from app.api.viewsets.movie_director_viewsets import MovieDirectorViewSet
from app.api.viewsets.movie_director_assignment_viewsets import MovieDirectorAssignmentViewSet
from app.api.viewsets.rating_viewsets import RatingViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for the project.",
        terms_of_service="https://www.yourproject.com/terms/",
        contact=openapi.Contact(email="agvan.bedrosian@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True, #Change to false if we dont want docs to be public
    permission_classes=(permissions.AllowAny,), #Change to permissions.IsAuthenticated
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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
