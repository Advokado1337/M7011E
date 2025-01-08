from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction


from app.models import Category, MovieCategory
from app.api.serializers.movie_serializer import (
     CategorySerializer
)
from app.decorators import token_and_superuser_required, token_and_isstaff_required



class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Categories.
    """
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @token_and_isstaff_required
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new category.
        """
        category_data = request.data

        if 'category' not in category_data:
            return Response({'error': 'Category is required'}, status=400)

        if 'category' in category_data and Category.objects.filter(category=category_data['category']).exists():
            return Response({'error': 'Category already exists'}, status=400)

        category_serializer = CategorySerializer(data={'category': category_data['category']})
        if category_serializer.is_valid():
            category_serializer.save()  # Save category instance
        else:
            return Response(category_serializer.errors, status=400)

        return Response(category_serializer.data, status=201)

    @token_and_superuser_required
    def destroy(self, request, pk=None):
        """
        Delete a category by ID.
        """
        if pk is None:
            return Response({'error': 'Category ID is required'}, status=400)
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)

        MovieCategory.objects.filter(category=category).delete()
        category.delete()
        return Response({'message': 'Category deleted!'}, status=200)