# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriesViewSet,
    SubCategoriesViewSet,
    TagsViewSet,
    TechniquesViewSet,
    TechniqueCategoriesViewSet,
    TechniqueTagsViewSet,
    SubTechniquesViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'subcategories', SubCategoriesViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'techniques', TechniquesViewSet)
router.register(r'technique-categories', TechniqueCategoriesViewSet)
router.register(r'technique-tags', TechniqueTagsViewSet)
router.register(r'subtechniques', SubTechniquesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
