from django.shortcuts import render, redirect
from .forms import ParentRegistrationForm, ChildStressForm, ParentStressForm
import joblib
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'stress_app/home.html')

def parent_register(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ParentRegistrationForm()
    return render(request, 'stress_app/parent_registration.html', {'form': form})
    
@login_required
def child_form_view(request):
    form = ChildStressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        request.session['child_data'] = [form.cleaned_data[f'q{i}'] for i in range(1, 14)]
        return redirect('result')
    return render(request, 'stress_app/child_form.html', {'form': form})

@login_required
def parent_form_view(request):
    form = ParentStressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        request.session['parent_data'] = [form.cleaned_data[f'q{i}'] for i in range(1, 14)]
        return redirect('result')
    return render(request, 'stress_app/parent_form.html', {'form': form})

child_model_path = os.path.join(settings.BASE_DIR, 'mental_health_app', 'ML', 'child_model.pkl')
parent_model_path = os.path.join(settings.BASE_DIR, 'mental_health_app', 'ML', 'parent_model.pkl')

child_model = joblib.load(child_model_path)
parent_model = joblib.load(parent_model_path)

def predict_stress(child_data, parent_data):
    child_stress = child_model.predict([child_data])
    parent_stress = parent_model.predict([parent_data])
    return child_stress, parent_stress

@login_required
def result_view(request):
    child_data = request.session.get('child_data', [0]*13)
    parent_data = request.session.get('parent_data', [0]*13)
    child_stress, parent_stress = predict_stress(child_data, parent_data)
    return render(request, 'stress_app/result.html', {
        'child_stress': child_stress[0],   
        'parent_stress': parent_stress[0]  
    })

@login_required
def parent_dashboard(request):
    return render(request, 'stress_app/parent_dashboard.html')

@login_required
def child_dashboard(request):
    return render(request, 'stress_app/child_dashboard.html')

@login_required
def login_redirect(request):
    profile = request.user.userprofile
    if profile.role == 'parent':
        return redirect('parent_dashboard')
    elif profile.role == 'child':
        return redirect('child_dashboard')
    else:
        return redirect('home')

