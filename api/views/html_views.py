# api/views/html_views.py

from django.shortcuts import render, redirect
from ..models import Technique
from ..forms import TechniqueForm
from django.contrib import messages
from django.core.paginator import Paginator

def techniques_list(request):
    technique_list = Technique.objects.all()
    paginator = Paginator(technique_list, 10)  # Show 10 techniques per page

    page_number = request.GET.get('page')
    techniques = paginator.get_page(page_number)
    return render(request, 'api/techniques_list.html', {'techniques': techniques})

def technique_add(request):
    if request.method == 'POST':
        form = TechniqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Technique added successfully!')
            return redirect('html_views:techniques_list')  # Use the namespace here
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TechniqueForm()
    return render(request, 'api/technique_add.html', {'form': form})

def home(request):
    return render(request, 'api/home.html')