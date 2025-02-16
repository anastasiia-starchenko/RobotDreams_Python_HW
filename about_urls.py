from django.urls import path
from .views import whoami

urlpatterns = [
    path('whoami/', whoami, name='whoami'),
]
from django.urls import path
from .views import whoami

urlpatterns = [
    path('whoami/', whoami, name='whoami'),
]