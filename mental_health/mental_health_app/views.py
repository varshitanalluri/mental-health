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
        stress_numeric = child_model.predict([child_data])[0]
        stress_label = child_encoder.inverse_transform([stress_numeric])[0]
        stress_label = stress_label.title()
        StressResult.objects.update_or_create(user=request.user, defaults={'stress_level': stress_label})
        return redirect('dashboard')
    return render(request, 'stress_app/child_form.html', {'form': form})

@login_required
@role_required(['parent'])
def parent_form_view(request):
    form = ParentStressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        parent_data = [form.cleaned_data[f'q{i}'] for i in range(1, 14)]
        stress_numeric = parent_model.predict([parent_data])[0]
        stress_label = parent_encoder.inverse_transform([stress_numeric])[0]
        stress_label = stress_label.title()
        StressResult.objects.update_or_create(user=request.user, defaults={'stress_level': stress_label})
        return redirect('dashboard')
    return render(request, 'stress_app/parent_form.html', {'form': form})

child_model_path = os.path.join(settings.BASE_DIR, 'mental_health_app', 'ML', 'child_model.pkl')
parent_model_path = os.path.join(settings.BASE_DIR, 'mental_health_app', 'ML', 'parent_model.pkl')
child_encoder_path = os.path.join(settings.BASE_DIR, 'mental_health_app', 'ML', 'label_encoder_child.pkl')
parent_encoder_path = os.path.join(settings.BASE_DIR, 'mental_health_app', 'ML', 'label_encoder_parent.pkl')

child_model = joblib.load(child_model_path)
parent_model = joblib.load(parent_model_path)
child_encoder = joblib.load(child_encoder_path)
parent_encoder = joblib.load(parent_encoder_path)

def predict_stress(child_data, parent_data):
    child_stress = child_model.predict([child_data])
    parent_stress = parent_model.predict([parent_data])
    return child_stress, parent_stress

@login_required
def login_redirect(request):
    return redirect('dashboard')

PRESCRIPTIONS = {
    ('parent', 'Very Low'): "Your child is doing very well. Keep supporting them!",
    ('parent', 'Low'): "Your child is managing stress fairly well. Keep an eye and encourage open conversations.",
    ('parent', 'Medium'): "Your child shows moderate stress. Consider spending more quality time with them.",
    ('parent', 'High'): "Your child is experiencing high stress. Try to understand their challenges and consider professional advice.",
    ('parent', 'Very High'): "Your child is under severe stress. Immediate consultation with a specialist is recommended.",

    ('child', 'Very Low'): "You are doing great! Keep maintaining your good habits.",
    ('child', 'Low'): "Stress is low. Remember to take breaks and relax regularly.",
    ('child', 'Medium'): "Moderate stress detected. Practice mindfulness or talk to someone you trust.",
    ('child', 'High'): "High stress detected. Please consider talking to a counselor or trusted adult.",
    ('child', 'Very High'): "Severe stress detected. Immediate help from a healthcare professional is advised.",
}

@login_required
def dashboard(request):
    profile = request.user.userprofile
    own_result = None
    prescription_msg = None 
    linked_results = []
    try:
        own_result = StressResult.objects.get(user=request.user)
        prescription_msg = PRESCRIPTIONS.get((profile.role, own_result.stress_level), "No advice available.")
    except StressResult.DoesNotExist:
        own_result = None
        prescription_msg = None
    if profile.role == 'parent':
        children = UserProfile.objects.filter(linked_parent=request.user, role='child')
        for child_profile in children:
            try:
                res = StressResult.objects.get(user=child_profile.user)
                linked_results.append({
                    'user': child_profile.user.username,
                    'role': 'Child',
                    'stress_level': res.stress_level,
                    'updated_at': res.updated_at
                })
            except StressResult.DoesNotExist:
                linked_results.append({
                    'user': child_profile.user.username,
                    'role': 'Child',
                    'stress_level': None,
                    'updated_at': None
                })
    elif profile.role == 'child':
        parent_profile = profile.linked_parent.userprofile if profile.linked_parent else None
        if parent_profile:
            try:
                res = StressResult.objects.get(user=profile.linked_parent)
                linked_results.append({
                    'user': profile.linked_parent.username,
                    'role': 'Parent',
                    'stress_level': res.stress_level,
                    'updated_at': res.updated_at
                })
            except StressResult.DoesNotExist:
                linked_results.append({
                    'user': profile.linked_parent.username,
                    'role': 'Parent',
                    'stress_level': None,
                    'updated_at': None
                })
    return render(request, 'stress_app/dashboard.html', {
        'own_result': own_result,
        'prescription_msg': prescription_msg,
        'linked_results': linked_results,
        'role': profile.role,
    })

def about_view(request):
    return render(request, 'stress_app/about.html')
