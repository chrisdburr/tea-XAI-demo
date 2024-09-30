# api/forms.py

from django import forms
from .models import Technique, Category, SubCategory, AssuranceGoal

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
    
    model_dependency = forms.ChoiceField(choices=[('agnostic', 'Agnostic'), ('specific', 'Specific')], widget=forms.RadioSelect)
    
    # Override to filter categories based on selected assurance goal
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'assurance_goal' in self.data:
            try:
                assurance_goal_id = int(self.data.get('assurance_goal'))
                self.fields['categories'].queryset = Category.objects.filter(assurance_goal_id=assurance_goal_id)
            except (ValueError, TypeError):
                pass  # invalid input, ignore and fallback to empty queryset
        else:
            self.fields['categories'].queryset = Category.objects.none()

        if 'categories' in self.data:
            try:
                category_id = int(self.data.get('categories'))
                self.fields['sub_categories'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass  # invalid input, ignore and fallback to empty queryset
        else:
            self.fields['sub_categories'].queryset = SubCategory.objects.none()