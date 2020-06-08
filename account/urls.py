from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register-page'),
    path('profile/', views.profile, name='profile'),
    path('profile/<id>/', views.profile_update, name='profile-update'),
    path('admin-dashboard/', views.profile, name='admin-dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login-page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='athletix/home.html'), name='logout-page')
]