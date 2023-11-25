from django.urls import path, include
from user.views import signup_view, activation_sent_view, activate
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path("", include("django.contrib.auth.urls")),
    path('signup/', signup_view, name="signup"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]