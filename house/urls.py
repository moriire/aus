from django.urls import path, include
from .views import all_houses, house

urlpatterns = [
    path('', all_houses, name='properties'),
    path('<str:pk>/', house, name='property')
]
