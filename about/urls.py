from django.urls import path
from . import views

urlpatterns = [
    path('', views.aboutPage, name='about-page')
]