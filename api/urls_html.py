# api/urls_html.py

from django.urls import path
from .views.html_views import home, techniques_list, technique_add

app_name = 'html_views'  # Ensure this line exists

urlpatterns = [
    path('', home, name='home'),  # Home page at '/'
    path('techniques/', techniques_list, name='techniques_list'),
    path('techniques/add/', technique_add, name='technique_add'),
]