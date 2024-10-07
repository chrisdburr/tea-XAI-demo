# api/models.py

from django.db import models
from django.core.exceptions import ValidationError

class AssuranceGoal(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'assurance_goal'
        verbose_name_plural = "Assurance Goals"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if AssuranceGoal.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'AssuranceGoal with this name already exists.'})

    def natural_key(self):
        return (self.name,)

    @classmethod
    def get_by_natural_key(cls, name):
        return cls.objects.get(name=name)

class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    assurance_goal = models.ForeignKey(AssuranceGoal, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if Category.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'Category with this name already exists.'})
    
    def natural_key(self):
        return (self.name,)

    @classmethod
    def get_by_natural_key(cls, name):
        return cls.objects.get(name=name)

class SubCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = "Sub-Categories"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if SubCategory.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'SubCategory with this name already exists.'})

    def natural_key(self):
        return (self.name, self.category.name)

    natural_key.dependencies = ['api.category']

    @classmethod
    def get_by_natural_key(cls, name, category_name):
        category = Category.objects.get_by_natural_key(category_name)
        return cls.objects.get(name=name, category=category)
    
class FairnessApproach(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'fairness_approach'
        verbose_name_plural = "Fairness Approaches"

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        if FairnessApproach.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'FairnessApproach with this name already exists.'})

class ProjectLifecycleStage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'project_lifecycle_stage'
        verbose_name_plural = "Project Lifecycle Stages"

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        if ProjectLifecycleStage.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'ProjectLifecycleStage with this name already exists.'})

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'tag'
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if Tag.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'Tag with this name already exists.'})

class Technique(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    assurance_goal = models.ForeignKey(AssuranceGoal, on_delete=models.CASCADE)
    model_dependency = models.CharField(max_length=255)
    example_use_case = models.TextField()
    scope = models.CharField(max_length=255, blank=True, null=True)  # Applicable only to explainability techniques
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, through='TechniqueTag', blank=True)
    reference = models.URLField(blank=True)
    software_package = models.URLField(blank=True)
    limitation = models.TextField(blank=True)
    fairness_approach = models.ManyToManyField(FairnessApproach, through='TechniqueFairnessApproach', blank=True)  # Applicable only to fairness techniques
    project_lifecycle_stage = models.ManyToManyField(ProjectLifecycleStage, through='TechniqueProjectLifecycleStage', blank=True) # Applicable only to fairness techniques

    class Meta:
        db_table = 'technique'
        verbose_name_plural = "Techniques"

    def clean(self):
        super().clean()
        if Technique.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'A technique with this name already exists.'})

    def __str__(self):
        return self.name

# class TechniqueCategory(models.Model):
#     technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'technique_category'
#         unique_together = ('technique', 'category')
#         verbose_name_plural = "Technique Categories"

# class TechniqueSubCategory(models.Model):
#     technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
#     sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'technique_sub_category'
#         unique_together = ('technique', 'sub_category')
#         verbose_name_plural = "Technique Sub-Categories"

class TechniqueTag(models.Model):
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'technique_tag'
        verbose_name_plural = "Technique Tags"
        unique_together = ('technique', 'tag')

    def __str__(self):
        return f"{self.technique.name} - {self.tag.name}"

class TechniqueFairnessApproach(models.Model):
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
    fairness_approach = models.ForeignKey(FairnessApproach, on_delete=models.CASCADE)

    class Meta:
        db_table = 'technique_fairness_approach'
        unique_together = ('technique', 'fairness_approach')

    def __str__(self):
        return f"{self.technique.name} - {self.fairness_approach.name}"

class TechniqueProjectLifecycleStage(models.Model):
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
    project_lifecycle_stage = models.ForeignKey(ProjectLifecycleStage, on_delete=models.CASCADE)

    class Meta:
        db_table = 'technique_project_lifecycle_stage'
        unique_together = ('technique', 'project_lifecycle_stage')

    def __str__(self):
        return f"{self.technique.name} - {self.project_lifecycle_stage.name}"
    
class TechniqueRelationship(models.Model):
    technique_from = models.ForeignKey(Technique, related_name='related_from', on_delete=models.DO_NOTHING, null=True, blank=True)
    technique_to = models.ForeignKey(Technique, related_name='related_to', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'technique_relationship'