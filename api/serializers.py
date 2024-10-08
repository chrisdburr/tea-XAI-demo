# api/serializers.py

from rest_framework import serializers
from .models import (
    AssuranceGoal,
    Category,
    SubCategory,
    FairnessApproach,
    ProjectLifecycleStage,
    Tag,
    Technique,
)

class AssuranceGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssuranceGoal
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['__all__']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['__all__']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
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
    category = CategorySerializer(read_only=True)
    sub_category = SubCategorySerializer(read_only=True)
    fairness_approaches = FairnessApproachSerializer(read_only=True)
    project_lifecycle_stages = ProjectLifecycleStageSerializer(read_only=True)

    class Meta:
        model = Technique
        fields = '__all__'