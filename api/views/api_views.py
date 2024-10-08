# api/views/api_views.py

from rest_framework import viewsets, filters
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from ..models import (
    AssuranceGoal,
    Category,
    SubCategory,
    FairnessApproach,
    ProjectLifecycleStage,
    Tag,
    Technique,
)
from ..serializers import (
    AssuranceGoalSerializer,
    CategorySerializer,
    SubCategorySerializer,
    FairnessApproachSerializer,
    ProjectLifecycleStageSerializer,
    TagSerializer,
    TechniqueSerializer,
)

class AssuranceGoalsViewSet(viewsets.ModelViewSet):
    queryset = AssuranceGoal.objects.all()
    serializer_class = AssuranceGoalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'assurance_goal']
    search_fields = ['name', 'assurance_goal__name']
    ordering_fields = ['id', 'name']

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'category']
    search_fields = ['name', 'category__name']
    ordering_fields = ['id', 'name']

def get_categorylist(request, assurance_goal_id):
    categorylist = Category.objects.filter(assurance_goal_id=assurance_goal_id)
    return JsonResponse({'categorylist': [{'id': category.id, 'name': category.name} for category in categorylist]})

def get_subcategorylist(request, category_id):
    sub_categorylist = SubCategory.objects.filter(category_id=category_id)
    return JsonResponse({'sub_categorylist': [{'id': sub_category.id, 'name': sub_category.name} for sub_category in sub_categorylist]})

class FairnessApproachesViewSet(viewsets.ModelViewSet):
    queryset = FairnessApproach.objects.all()
    serializer_class = FairnessApproachSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']

class ProjectLifecycleStagesViewSet(viewsets.ModelViewSet):
    queryset = ProjectLifecycleStage.objects.all()
    serializer_class = ProjectLifecycleStageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
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
        'category',
        'sub_category',
        'model_dependency',
        'scope', 
    ]
    search_fields = ['name', 'description', 'example_use_case']
    ordering_fields = ['id', 'name']
