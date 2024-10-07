# api/forms.py

from django import forms
from .models import Technique, Category, SubCategory

class TechniqueForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = [
            'name',
            'description',
            'assurance_goal',
            'category',
            'sub_category',
            'model_dependency',
            'example_use_case',
            'tags',
            'reference',
            'software_package',
            'limitation',
            'fairness_approach',
            'project_lifecycle_stage',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'example_use_case': forms.Textarea(attrs={'rows': 3}),
            'limitation': forms.Textarea(attrs={'rows': 3}),
            'fairness_approach': forms.SelectMultiple(attrs={'id': 'id_fairness_approach'}),
            'project_lifecycle_stage': forms.SelectMultiple(attrs={'id': 'id_project_lifecycle_stage'}),
            'tags': forms.SelectMultiple(attrs={'id': 'id_tags'}),
            'category': forms.Select(attrs={'id': 'id_category'}),
            'sub_category': forms.Select(attrs={'id': 'id_sub_category'}),
        }
    
    model_dependency = forms.ChoiceField(choices=[('agnostic', 'Agnostic'), ('specific', 'Specific')], widget=forms.RadioSelect)
    
    # Override to filter category based on selected assurance goal
    def __init__(self, *args, **kwargs):
        super(TechniqueForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()
        self.fields['sub_category'].queryset = SubCategory.objects.none()

        if 'assurance_goal' in self.data:
            try:
                assurance_goal_id = int(self.data.get('assurance_goal'))
                self.fields['category'].queryset = Category.objects.filter(assurance_goal_id=assurance_goal_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Category queryset
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.assurance_goal.category_set.order_by('name')

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty SubCategory queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.order_by('name')