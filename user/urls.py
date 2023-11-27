from django.urls import path, include
from user.views import IndexView, AboutView, ContactView, signup_view, activation_sent_view, activate
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("", include("django.contrib.auth.urls")),
    path('signup/', signup_view, name="signup"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]