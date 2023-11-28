from django_unicorn.components import UnicornView
from house.models import House
from django.core.paginator import Paginator
from django.db.models import Count


class FilterView(UnicornView):
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

"""
<div>
    <div class="columns">
        <div class="column is-two-thirds">
            <div class="field">
                <label class="label">Category</label>
                <div class="control">
                    <div class="select">
                    <select unicorn:model.defer="category">
                        {% for cat in categories %}
                            <option value="{{ cat.id }}">{{ cat.title }}</option>
                        {% endfor %}
                    </select>
                    </div>
                </div>
            </div>
            <div class="field is-grouped">
            <div class="control">
                <button class="button is-link" unicorn:click="movies_search_button">Search</button>
            </div>
            {% if movies_search_flag %}
            <div class="control">
                <button class="button is-link is-light" unicorn:click="$reset">Restore</button>
            </div>
            {% endif %}
            </div>
        </div>
    </div>

    {% if page.object_list %}

    <div class="table-container">
        <table class="table is-bordered is-striped is-hoverable is-fullwidth">
            <thead>
                <tr>
                <th><abbr title="Title">Title</abbr></th>
                <th><abbr title="Genre">Genre</abbr></th>
                <th><abbr title="Year">Year</abbr></th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                <th><abbr title="Title">Title</abbr></th>
                <th><abbr title="Genre">Genre</abbr></th>
                <th><abbr title="Year">Year</abbr></th>
                </tr>
            </tfoot>
            <tbody>
            {% for i in page.object_list %}
                <tr>
                <th>{{ i.title }}</th>
                <td>{{ i.genre }}</td>
                <td>{{ i.year }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>

    {% if page.paginator.num_pages > 1 %}
        <nav class="pagination" role="navigation" aria-label="pagination">
        {% if page.has_previous %}
            <a class="pagination-previous" unicorn:click="go_to_page({{ page.previous_page_number }})">Previous</a>
        {% else %}
            <a class="pagination-previous" disabled>Previous</a>
        {% endif %}
        {% if page.has_next %}
            <a class="pagination-next" unicorn:click="go_to_page({{ page.next_page_number }})">Next page</a>
        {% else %}
            <a class="pagination-next" disabled>Next page</a>
        {% endif %}
        <ul class="pagination-list">
            {% for i in page_range|default_if_none:page.paginator.get_elided_page_range %}
                {% if page.number == i %}
                    <li>
                        <a class="pagination-link is-current" aria-label="Page {{ i }}" aria-current="page">{{ i }}</a>
                    </li>
                {% else %}
                    {% if i == page.paginator.ELLIPSIS %}
                        <li>
                            <span class="pagination-ellipsis">{{ i }}</span>
                        </li>
                    {% else %}
                        <a class="pagination-link" unicorn:click="go_to_page({{ i }})" aria-label="Page {{ i }}" aria-current="page">{{ i }}</a>
                    </li>
                    {% endif %}
                {% endif %}
            {% endfor %}
        </ul>
        </nav>
    {% endif %}
    {% else %}
        <div class="notification is-danger is-light">
        {% comment %} <button class="delete"></button> {% endcomment %}
        No results found.
        </div>
    {% endif %}
</div>

"""
