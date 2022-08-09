from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Myapp-Home'),
    path('about/', views.about, name='Myapp-about'),
    
]
