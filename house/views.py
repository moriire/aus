from django.shortcuts import render
from .models import House

def all_houses(request):
    houses = House.objects.select_related('agent')
    return render(request, "all_houses.html", {'houses': houses})

def house(request, pk):
    house = House.objects.select_related('agent').get(id=pk)
    return render(request, "house.html", {'House': house})