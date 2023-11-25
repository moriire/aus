from django_unicorn.components import UnicornView

class StateView(UnicornView):
    def all_states(self):
        return ["Alabama", "Alaska", "Arizona"]