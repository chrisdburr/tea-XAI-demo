# api/views/api_views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import (
    AssuranceGoal,
    Category,
    SubCategory,
    Tag,
    Technique,
    Property,
    TechniqueProperty,
    TechniqueTag,
)
from ..serializers import (
    AssuranceGoalSerializer,
    CategorySerializer,
    SubCategorySerializer,
    TagSerializer,
    TechniqueSerializer,
    PropertySerializer,
    TechniquePropertySerializer,
    TechniqueTagSerializer,
)

# New ViewSet for AssuranceGoal
class AssuranceGoalsViewSet(viewsets.ModelViewSet):
    queryset = AssuranceGoal.objects.all()
    serializer_class = AssuranceGoalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name']

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'assurance_goal']
    search_fields = ['name', 'assurance_goal__name']
    ordering_fields = ['id', 'name']

class SubCategoriesViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'category']
    search_fields = ['name', 'category__name']
    ordering_fields = ['id', 'name']

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']

class TechniquesViewSet(viewsets.ModelViewSet):
    queryset = Technique.objects.all()
    serializer_class = TechniqueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'name',
        'assurance_goal',
        'categories',
        'sub_categories',
        'model_dependency',
        'scope', 
    ]
    search_fields = ['name', 'description', 'example_use_case']
    ordering_fields = ['id', 'name']

class PropertiesViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'assurance_goal']
    search_fields = ['name', 'assurance_goal__name']
    ordering_fields = ['id', 'name']

class TechniquePropertiesViewSet(viewsets.ModelViewSet):
    queryset = TechniqueProperty.objects.all()
    serializer_class = TechniquePropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['technique', 'property', 'value']
    search_fields = ['technique__name', 'property__name', 'value']
    ordering_fields = ['technique', 'property']

class TechniqueTagsViewSet(viewsets.ModelViewSet):
    queryset = TechniqueTag.objects.all()
    serializer_class = TechniqueTagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['technique', 'tag']
    search_fields = ['technique__name', 'tag__name']
    ordering_fields = ['technique', 'tag']