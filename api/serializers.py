# api/serializers.py

from rest_framework import serializers
from .models import (
    Categories,
    SubCategories,
    Tags,
    Techniques,
    TechniqueCategories,
    TechniqueTags,
    SubTechniques,
)

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']

    def validate_name(self, value):
        normalized_name = value.strip().title()
        if Categories.objects.filter(name__iexact=normalized_name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return normalized_name

    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].title()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = validated_data['name'].title()
        return super().update(instance, validated_data)


class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = ['id', 'name']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']


class TechniquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Techniques
        fields = [
            'id',
            'technique',
            'description',
            'scope_global',
            'scope_local',
            'model_dependency',
            'example_use_case',
        ]


class TechniqueCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueCategories
        fields = ['technique', 'category']  # Removed 'id'


class TechniqueTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueTags
        fields = ['technique', 'tag']  # Removed 'id'


class SubTechniquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTechniques
        fields = ['technique', 'sub_category']  # Removed 'id'
