from django_unicorn.components import UnicornView
from house.models import House
class SlidesView(UnicornView):
    houses = []#House.objects.none() 
    def mount(self):
        self.houses =  House.objects.all()
        #return super().mount()
