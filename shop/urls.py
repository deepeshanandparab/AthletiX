from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop-home-page'),
    path('item/', views.item, name='shop-item-page')
]