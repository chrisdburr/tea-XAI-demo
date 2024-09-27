# api/urls.py

from django.urls import path, include
from rest_framework import routers
from .views.api_views import (
    CategoriesViewSet,
    SubCategoriesViewSet,
    TagsViewSet,
    TechniquesViewSet,
    TechniqueCategoriesViewSet,
    TechniqueTagsViewSet,
    SubTechniquesViewSet,
)

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'subcategories', SubCategoriesViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'techniques', TechniquesViewSet)
router.register(r'techniquecategories', TechniqueCategoriesViewSet)
router.register(r'techniquetags', TechniqueTagsViewSet)
router.register(r'subtechniques', SubTechniquesViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API endpoints
]