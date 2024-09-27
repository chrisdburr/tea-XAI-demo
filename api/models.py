# api/models.py
from django.db import models
from django.core.exceptions import ValidationError

class Categories(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'categories'

    def clean(self):
        if Categories.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'Category with this name already exists.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SubCategories(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'sub_categories'

    def clean(self):
        if SubCategories.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'SubCategory with this name already exists.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'tags'

    def clean(self):
        if Tags.objects.filter(name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'Tag with this name already exists.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Techniques(models.Model):
    technique = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    scope_global = models.BooleanField(blank=True, null=True)
    scope_local = models.BooleanField(blank=True, null=True)
    model_dependency = models.CharField(max_length=50, blank=True, null=True)
    example_use_case = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Categories, through='TechniqueCategories', related_name='techniques')
    tags = models.ManyToManyField(Tags, through='TechniqueTags', related_name='techniques')

    class Meta:
        db_table = 'techniques'
        indexes = [
            models.Index(fields=['technique'], name='techniques_technique_idx'),
        ]

    def clean(self):
        if Techniques.objects.filter(technique__iexact=self.technique).exclude(id=self.id).exists():
            raise ValidationError({'technique': 'Technique with this name already exists.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TechniqueCategories(models.Model):
    technique = models.ForeignKey(Techniques, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'technique_categories'
        unique_together = (('technique', 'category'),)


class TechniqueTags(models.Model):
    technique = models.ForeignKey(Techniques, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        db_table = 'technique_tags'
        unique_together = (('technique', 'tag'),)


class SubTechniques(models.Model):
    technique = models.ForeignKey(Techniques, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_techniques'
        unique_together = (('technique', 'sub_category'),)