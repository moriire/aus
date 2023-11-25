from django.shortcuts import render
from .models import Agent
def index(request):
    context = {"hello": {"world": {"name": "Galaxy"}}}
    return render(request, "agent/index.html", context)

def all_agents(request):
    agents = Agent.objects.select_related('user')
    return render(request, "all_agents.html", {'agents': agents})

def agent(request, pk):
    agent = Agent.objects.select_related('user').get(id=pk)
    return render(request, "agent.html", {'agent': agent})