# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/', include('api.urls')),  # API endpoints
    path('', include('api.urls_html')),  # HTML views including home
]