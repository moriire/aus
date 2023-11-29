from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token
from user.models import User
from django_unicorn.components import LocationUpdate,  HashUpdate, UnicornView
from house.models import House
from agent.models import Agent

class IndexView(UnicornView):
    template_name = "index.html"
    properties:House = []
    agents:Agent = []
    search = {'keyword': '', 'city': '', 'prop_type': '', 'bedrooms': 1, 'garages': 2, 'price': 0}

    def for_search(self):
        return  LocationUpdate(redirect('/login/'))# redirect('login')
    def make(self):
        return HashUpdate(f"#hi")
    
    def mount(self):
        self.properties = House.objects.filter(goal="rent")[:6]
        self.agents = Agent.objects.all()[:6]

class AboutView(UnicornView):
    template_name = "about.html"

class ContactView(UnicornView):
    template_name = "contact.html"

def activation_sent_view(request):
    return render(request, 'activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.user_agent.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'user/activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            #user.user_agent.first_name = form.cleaned_data.get('first_name')
            #user.user_agent.last_name = form.cleaned_data.get('last_name')
            #user.user_agent.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

