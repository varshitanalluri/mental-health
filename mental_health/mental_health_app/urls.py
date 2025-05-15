from django.urls import path
from django.contrib.auth import views as auth_views
from mental_health_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parent-register/', views.parent_register, name='parent_register'),
    path('login/', auth_views.LoginView.as_view(template_name='stress_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('child-form/', views.child_form_view, name='child_form'),
    path('parent-form/', views.parent_form_view, name='parent_form'),
    path('result/', views.result_view, name='result'),
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('child-dashboard/', views.child_dashboard, name='child_dashboard'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
]