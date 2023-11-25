from django.urls import path, include
from .views import all_agents, agent

urlpatterns = [
    path('', all_agents, name='agents'),
    path('<str:pk>/', agent, name='agent')
]
