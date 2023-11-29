from django.urls import path, include
from .views import house, PropertiesView

urlpatterns = [
    path('', PropertiesView.as_view(), name='properties'),
    path('<str:pk>/', house, name='property')
]