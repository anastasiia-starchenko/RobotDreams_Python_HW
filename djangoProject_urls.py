from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('courses/', include('myapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)