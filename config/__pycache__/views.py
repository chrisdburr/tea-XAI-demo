# api/views.py

from django.shortcuts import render, redirect
from .models import Techniques
from .forms import TechniqueForm  # Ensure you have this form defined

def techniques_list(request):
    techniques = Techniques.objects.all()
    return render(request, 'api/techniques_list.html', {'techniques': techniques})

def technique_add(request):
    if request.method == 'POST':
        form = TechniqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('techniques_list')
    else:
        form = TechniqueForm()
    return render(request, 'api/technique_add.html', {'form': form})