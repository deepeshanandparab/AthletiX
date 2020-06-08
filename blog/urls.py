from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome, name='blog-page'),
]