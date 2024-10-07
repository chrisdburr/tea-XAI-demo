# api/urls.py

from django.urls import path
from .views.html_views import (
    techniques_list,
    technique_add,
    technique_detail,
    home,
    get_categories,
    get_subcategories,
)

app_name = 'html_views'

urlpatterns = [
    path('', home, name='home'),
    path('techniques/', techniques_list, name='techniques_list'),
    path('techniques/add/', technique_add, name='technique_add'),
    path('techniques/<int:technique_id>/', technique_detail, name='technique_detail'),
    path('get_categories/<int:assurance_goal_id>/', get_categories, name='get_categories'),
    path('get_subcategories/<int:category_id>/', get_subcategories, name='get_subcategories'),
]