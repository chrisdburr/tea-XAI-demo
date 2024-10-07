# api/views/html_views.py

from django.shortcuts import render, redirect
from ..models import (
    Technique, AssuranceGoal, Category, SubCategory, FairnessApproach,
    ProjectLifecycleStage, Tag
)
from ..forms import TechniqueForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest

def techniques_list(request):
    assurance_goal_filter = request.GET.get('assurance_goal')
    category_filter = request.GET.get('category')
    technique_list = Technique.objects.all()

    if assurance_goal_filter:
        technique_list = technique_list.filter(assurance_goal__id=assurance_goal_filter)

    if category_filter:
        technique_list = technique_list.filter(category__id=category_filter)

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
            technique = form.save()
            form.save_m2m()  # Save ManyToMany relationships like tags
            messages.success(request, 'Technique added successfully!')
            return redirect('html_views:techniques_list') 
        else:
            messages.error(request, 'Please correct the errors below.')
            # Populate categories and subcategories based on form data
            assurance_goal_id = request.POST.get('assurance_goal')
            category_id = request.POST.get('category')
            categories = Category.objects.filter(assurance_goal_id=assurance_goal_id) if assurance_goal_id else []
            sub_categories = SubCategory.objects.filter(category_id=category_id) if category_id else []
    else:
        form = TechniqueForm()
        categories = []
        sub_categories = []

    # Retrieve fairness approaches and project lifecycle stages
    fairness_approaches = FairnessApproach.objects.all().order_by('name')
    project_lifecycle_stages = ProjectLifecycleStage.objects.all().order_by('name')

    return render(request, 'api/technique_add.html', {
        'form': form,
        'fairness_approaches': fairness_approaches,
        'project_lifecycle_stages': project_lifecycle_stages,
        'categories': categories,
        'sub_categories': sub_categories,
        'selected_category': request.POST.get('category') if request.method == 'POST' else '',
        'selected_sub_category': request.POST.get('sub_category') if request.method == 'POST' else '',
    })

def technique_detail(request, technique_id):
    technique = Technique.objects.get(id=technique_id)
    return render(request, 'api/technique_detail.html', {'technique': technique})

def home(request):
    return render(request, 'api/home.html')

# AJAX Endpoints for fetching categories and subcategories
def get_categories(request, assurance_goal_id):
    try:
        assurance_goal = AssuranceGoal.objects.get(id=assurance_goal_id)
    except AssuranceGoal.DoesNotExist:
        return HttpResponseBadRequest("Invalid Assurance Goal ID")

    categories = Category.objects.filter(assurance_goal=assurance_goal).values('id', 'name')
    return JsonResponse({'categories': list(categories)})

def get_subcategories(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return HttpResponseBadRequest("Invalid Category ID")

    sub_categories = SubCategory.objects.filter(category=category).values('id', 'name')
    return JsonResponse({'sub_categories': list(sub_categories)})