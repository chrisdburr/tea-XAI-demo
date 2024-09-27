# api/forms.py

from django import forms
from .models import Techniques

class TechniqueForm(forms.ModelForm):
    class Meta:
        model = Techniques
        fields = [
            'technique',
            'description',
            'scope_global',
            'scope_local',
            'model_dependency',
            'example_use_case',
            'categories',
            'tags',
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'tags': forms.CheckboxSelectMultiple(),
        }