# api/views/html_views.py

from django.shortcuts import render, redirect
from ..models import Technique, AssuranceGoal, Category
from ..forms import TechniqueForm
from django.contrib import messages
from django.core.paginator import Paginator

def techniques_list(request):
    assurance_goal_filter = request.GET.get('assurance_goal')
    category_filter = request.GET.get('category')
    technique_list = Technique.objects.all()

    if assurance_goal_filter:
        technique_list = technique_list.filter(assurance_goal__id=assurance_goal_filter)

    if category_filter:
        technique_list = technique_list.filter(categories__id=category_filter)

    paginator = Paginator(technique_list, 10)  # Show 10 techniques per page
    page_number = request.GET.get('page')
    techniques = paginator.get_page(page_number)

    return render(request, 'api/techniques_list.html', {
        'techniques': techniques,
        'categories': Category.objects.all(),  # Pass all categories to the template
        'assurance_goals': AssuranceGoal.objects.all(),  # Pass all assurance goals to the template
        'selected_category': category_filter,
        'selected_assurance_goal': assurance_goal_filter  # Pass the selected assurance goal
    })

def technique_add(request):
    if request.method == 'POST':
        form = TechniqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Technique added successfully!')
            return redirect('html_views:techniques_list') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TechniqueForm()
    return render(request, 'api/technique_add.html', {'form': form})

def technique_detail(request, technique_id):
    technique = Technique.objects.get(id=technique_id)
    return render(request, 'api/technique_detail.html', {'technique': technique})

def home(request):
    return render(request, 'api/home.html')