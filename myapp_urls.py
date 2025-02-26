from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Головна сторінка
    path('register/', views.register, name='register'),  # Реєстрація
    path('login/', views.user_login, name='login'),  # Логін
    path('logout/', views.user_logout, name='logout'),  # Логаут
]