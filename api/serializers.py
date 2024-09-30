# api/serializers.py

from rest_framework import serializers
from .models import (
    AssuranceGoal,
    Category,
    SubCategory,
    Tag,
    Technique,
    Property,
    TechniqueProperty,
    TechniqueTag,
    FairnessApproach,
    ProjectLifecycleStage,
)

class AssuranceGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssuranceGoal
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'assurance_goal']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'category']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class TechniquePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueProperty
        fields = '__all__'

class TechniqueTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueTag
        fields = '__all__'

class FairnessApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = FairnessApproach
        fields = '__all__'

class ProjectLifecycleStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLifecycleStage
        fields = '__all__'

class TechniqueSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    assurance_goal = AssuranceGoalSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    fairness_approaches = serializers.SerializerMethodField()
    project_lifecycle_stages = serializers.SerializerMethodField()

    class Meta:
        model = Technique
        fields = '__all__'

    def get_fairness_approaches(self, obj):
        return [fa.fairness_approach.name for fa in obj.techniquefairnessapproach_set.all()]

    def get_project_lifecycle_stages(self, obj):
        return [pls.project_lifecycle_stage.name for pls in obj.techniqueprojectlifecyclestage_set.all()]