# api/forms.py

from django import forms
from .models import Technique

class TechniqueForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = [
            'name',
            'description',
            'assurance_goal',
            'model_dependency',
            'example_use_case',
            'scope',
            'categories',
            'sub_categories',
            'tags',
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'sub_categories': forms.CheckboxSelectMultiple(),
            'tags': forms.CheckboxSelectMultiple(),
        }