from django_unicorn.components import UnicornView
from house.models import House
#from django.views.generic import ListView
from django.core.paginator import Paginator


class FilterView(UnicornView):
    selected = ""
    houses: House = House.objects.none()
    page_obj = ""

    def mount(self):
        self.houses = House.objects.all().select_related("agent")
        #self.pq

    def filtered(self):
        self.houses = House.objects.all().filter(goal=self.selected)
        #self.pq(request)

    def pq(self, request):
        paginator = Paginator(self.houses, 1)
        page_number = request.GET.get('page')
        self.page_obj = paginator.get_page(page_number)

