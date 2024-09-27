from django.contrib import admin

# Register your models here.

from .models import (
    Techniques,
    Categories,
    SubCategories,
    Tags,
    TechniqueCategories,
    TechniqueTags,
    SubTechniques
)

admin.site.register(Techniques)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Tags)
admin.site.register(TechniqueCategories)
admin.site.register(TechniqueTags)
admin.site.register(SubTechniques)