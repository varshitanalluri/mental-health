
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.parent_register, name='parent_register'),
    path('login/', auth_views.LoginView.as_view(template_name='stress_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('parent-form/', views.parent_form_view, name='parent_form'),
    path('child-form/', views.child_form_view, name='child_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path('about/', views.about_view, name='about'),  
    path('api/esp32/', views.esp32_data, name='esp32_data'),
    path('fitness-watch/', views.fitness_watch_view, name='fitness_watch'),
    path('api/esp32/latest/', views.latest_esp32_data, name='latest_esp32_data'),
]
