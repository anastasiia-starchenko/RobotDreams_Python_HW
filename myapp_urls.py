from django.urls import path
from myapp import views

urlpatterns = [
    path('registration_success/', views.registration_success, name='registration_success'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('reset/<uidb64>/<token>/', views.password_reset, name='password_reset'),
]