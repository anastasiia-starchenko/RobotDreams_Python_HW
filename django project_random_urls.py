from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the homepage! Go to /random/ for the random string generator.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', include('random_app.urls')),
    path('', home, name='home'),
]