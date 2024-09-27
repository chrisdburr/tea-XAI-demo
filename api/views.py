# api/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Categories,
    SubCategories,
    Tags,
    Techniques,
    TechniqueCategories,
    TechniqueTags,
    SubTechniques,
)
from .serializers import (
    CategoriesSerializer,
    SubCategoriesSerializer,
    TagsSerializer,
    TechniquesSerializer,
    TechniqueCategoriesSerializer,
    TechniqueTagsSerializer,
    SubTechniquesSerializer,
)

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']


class SubCategoriesViewSet(viewsets.ModelViewSet):
    queryset = SubCategories.objects.all()
    serializer_class = SubCategoriesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']


class TechniquesViewSet(viewsets.ModelViewSet):
    queryset = Techniques.objects.all()
    serializer_class = TechniquesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['technique', 'scope_global', 'scope_local']
    search_fields = ['technique', 'description', 'example_use_case']
    ordering_fields = ['id', 'technique']


class TechniqueCategoriesViewSet(viewsets.ModelViewSet):
    queryset = TechniqueCategories.objects.all()
    serializer_class = TechniqueCategoriesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['technique', 'category']
    search_fields = ['technique__technique', 'category__name']
    ordering_fields = ['technique', 'category']


class TechniqueTagsViewSet(viewsets.ModelViewSet):
    queryset = TechniqueTags.objects.all()
    serializer_class = TechniqueTagsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['technique', 'tag']
    search_fields = ['technique__technique', 'tag__name']
    ordering_fields = ['technique', 'tag']


class SubTechniquesViewSet(viewsets.ModelViewSet):
    queryset = SubTechniques.objects.all()
    serializer_class = SubTechniquesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['technique', 'sub_category']
    search_fields = ['technique__technique', 'sub_category__name']
    ordering_fields = ['technique', 'sub_category']
