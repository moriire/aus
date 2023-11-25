# hello_world.py
from django_unicorn.components import UnicornView

class HelloWorldView(UnicornView):
    name = "original"

    def mount(self):
        self.name = "mounted"