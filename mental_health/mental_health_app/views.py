from django.shortcuts import render, redirect
from .forms import ParentRegistrationForm, ChildStressForm, ParentStressForm
import joblib
import os
from django.conf import settings
from .models import StressResult, UserProfile
from .decorators import role_required
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
@role_required(['child'])
def child_form_view(request):
    form = ChildStressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        child_data = [form.cleaned_data[f'q{i}'] for i in range(1, 14)]
        child_stress = child_model.predict([child_data])[0]

        # Save or update stress result for this user
        StressResult.objects.update_or_create(user=request.user, defaults={'stress_level': child_stress})

        return redirect('dashboard')
    return render(request, 'stress_app/child_form.html', {'form': form})

@login_required
@role_required(['parent'])
def parent_form_view(request):
    form = ParentStressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        parent_data = [form.cleaned_data[f'q{i}'] for i in range(1, 14)]
        parent_stress = parent_model.predict([parent_data])[0]

        # Save or update stress result for this user
        StressResult.objects.update_or_create(user=request.user, defaults={'stress_level': parent_stress})

        return redirect('dashboard')
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
def login_redirect(request):
    return redirect('dashboard')

@login_required
def dashboard(request):
    profile = request.user.userprofile
    own_result = None
    linked_results = []

    try:
        own_result = StressResult.objects.get(user=request.user)
    except StressResult.DoesNotExist:
        own_result = None

    if profile.role == 'parent':
        children = UserProfile.objects.filter(linked_parent=request.user, role='child')
        for child_profile in children:
            try:
                res = StressResult.objects.get(user=child_profile.user)
                linked_results.append({'user': child_profile.user.username, 'role': 'Child', 'stress_level': res.stress_level})
            except StressResult.DoesNotExist:
                linked_results.append({'user': child_profile.user.username, 'role': 'Child', 'stress_level': None})
    elif profile.role == 'child':
        parent_profile = profile.linked_parent.userprofile if profile.linked_parent else None
        if parent_profile:
            try:
                res = StressResult.objects.get(user=profile.linked_parent)
                linked_results.append({'user': profile.linked_parent.username, 'role': 'Parent', 'stress_level': res.stress_level})
            except StressResult.DoesNotExist:
                linked_results.append({'user': profile.linked_parent.username, 'role': 'Parent', 'stress_level': None})

    return render(request, 'stress_app/dashboard.html', {
        'own_result': own_result,
        'linked_results': linked_results,
        'role': profile.role,
    })

def about_view(request):
    return render(request, 'stress_app/about.html')
