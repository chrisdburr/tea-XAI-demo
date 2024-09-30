# api/urls.py

from django.urls import path, include
from rest_framework import routers
from .views.api_views import (
    AssuranceGoalsViewSet,
    CategoriesViewSet,
    SubCategoriesViewSet,
    TagsViewSet,
    TechniquesViewSet,
    PropertiesViewSet,
    TechniquePropertiesViewSet,
    TechniqueTagsViewSet,
)

router = routers.DefaultRouter()
router.register(r'assurancegoals', AssuranceGoalsViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'subcategories', SubCategoriesViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'techniques', TechniquesViewSet)
router.register(r'properties', PropertiesViewSet)
router.register(r'techniqueproperties', TechniquePropertiesViewSet)
router.register(r'techniquetags', TechniqueTagsViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API endpoints
]