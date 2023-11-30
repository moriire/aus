from django_unicorn.components import UnicornView, LocationUpdate, HashUpdate
from django.shortcuts import render, redirect
from typing import Dict

class SearchView(UnicornView):
    #search_data:Dict = {'keyword': 'nnn', 'city': '', 'prop_type': '', 'bedrooms': 1, 'garages': 2, 'price': 0}
    keywords= ""
    city:str = ""
   
    
