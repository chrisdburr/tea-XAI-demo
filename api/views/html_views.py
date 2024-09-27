# api/views/html_views.py

from django.shortcuts import render, redirect
from ..models import Techniques
from ..forms import TechniqueForm 
from django.contrib import messages

def techniques_list(request):
    techniques = Techniques.objects.all()
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