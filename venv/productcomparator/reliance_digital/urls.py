from django.urls import path
from . import views

urlpatterns = [
    path('reliance_digitalapi', views.reliance_digitalapi),
    
]