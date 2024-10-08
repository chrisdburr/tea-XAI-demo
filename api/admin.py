from django.contrib import admin
from .models import (
    AssuranceGoal,
    Category,
    SubCategory,
    Technique,
    Tag,
    TechniqueTag,
    # TechniqueCategory,
    # TechniqueSubCategory,
    FairnessApproach,
    ProjectLifecycleStage,
    TechniqueFairnessApproach,
    TechniqueProjectLifecycleStage,
)

admin.site.register(Technique)
admin.site.register(AssuranceGoal)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)
admin.site.register(TechniqueTag)
# admin.site.register(TechniqueCategory)
# admin.site.register(TechniqueSubCategory)
admin.site.register(FairnessApproach)
admin.site.register(ProjectLifecycleStage)
admin.site.register(TechniqueFairnessApproach)
admin.site.register(TechniqueProjectLifecycleStage)