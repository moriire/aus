from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("unicorn/", include("django_unicorn.urls")),
    path('', include('user.urls')),
    path('agents/', include('agent.urls')),
    path('admin/', admin.site.urls),
]
