from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/search/', views.api_search, name='api_search'),
    path('api/animals/<int:pk>/', views.api_animal_detail, name='api_animal_detail'),
]
