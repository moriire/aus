from django.shortcuts import render
from django_unicorn.components import UnicornView
from .models import House
from django.core.paginator import Paginator
from django.db.models import Count

class PropertiesView(UnicornView):
    template_name = "all_houses.html"
    selected = ""
    houses: House = House.objects.none()
    page_obj = []


    items_per_page = 1
    page_index = 1
    paginator = None
    page = None
    page_range = None

    class Meta:
        exclude = ()
        javascript_exclude = (
            "paginator",
            "page",
            "page_range",
        )

    def mount(self):
        self.houses = House.objects.all().select_related("agent")
        self.paginator = Paginator(self.houses, self.items_per_page)
        
    def filtered(self, request):
        if self.selected == "":
            self.houses = House.objects.all().select_related("agent")
        else:
            self.houses = House.objects.select_related("agent").filter(goal=self.selected)
        self.paginator = Paginator(self.houses, self.items_per_page)
        self.route_page(self.current_page(request))

    def route_page(self, p):
        self.page = self.paginator.page(p)
        self.page_obj = self.page.object_list

    def current_page(self, request):
        p = request.Get.get('page')
        return p
    
def house(request, pk):
    house = House.objects.select_related('agent').get(id=pk)
    return render(request, "house.html", {'house': house})
