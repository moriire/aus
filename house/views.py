from django.shortcuts import render
from django_unicorn.components import UnicornView
from .models import House
from django.core.paginator import Paginator
from django.db.models import Count

class PropertiesView(UnicornView):
    template_name = "all_houses.html"
    selected = ""
    houses: House = House.objects.none()
    page_obj = ""


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

        self.page = self.paginator.page(self.page_index)
        self.page_range = self.paginator.get_elided_page_range(number=self.page_index, on_each_side=3, on_ends=2)

    def filtered(self):
        self.paginator = Paginator(self.houses, self.items_per_page)
        if self.selected == "":
            self.houses = House.objects.all().select_related("agent")
        else:
            self.houses = House.objects.select_related("agent").filter(goal=self.selected)

        self.page = self.paginator.page(self.page_index)
        self.page_range = self.paginator.get_elided_page_range(number=self.page_index, on_each_side=3, on_ends=2)


    def pq(self, request):
        paginator = Paginator(self.houses, 1)
        page_number = request.GET.get('page')
        self.page_obj = paginator.get_page(page_number)

    def houses_list(self):
        self.page = ''
        houses_search_flag = False
        paginator = Paginator(self.houses, self.items_per_page)
        self.paginator = paginator
        self.page = self.paginator.page(self.page_index)
        self.page_range = self.paginator.get_elided_page_range(number=self.page_index, on_each_side=3, on_ends=2)
        return self.page

    def go_to_page(self, page):
        print("go_to_page")
        self.page_index = page
   

    def houses_search_button(self):
        self.page_index = 1
        self.houses_search_flag = True
        self.houses_search()

    def houses_search(self):
        self.page = ''
        qs = House.objects.filter(goal=self.selected)
        paginator = Paginator(qs, self.items_per_page)
        self.paginator = paginator
        try:
            self.page = paginator.page(self.page_index)
            self.page_range = self.paginator.get_elided_page_range(number=self.page_index, on_each_side=3, on_ends=2)
            return self.page
        except EmptyPage:
            self.page = ''

def all_houses(request):
    #houses = House.objects.select_related('agent')
    return render(request, "all_houses.html", {})#, {'houses': houses})

def house(request, pk):
    house = House.objects.select_related('agent').get(id=pk)
    return render(request, "house.html", {'house': house})
