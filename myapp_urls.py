from django.urls import path
from .views import register, confirm_email, email_confirmation_message

urlpatterns = [
    path('register/', register, name='register'),
    path('accounts/confirm/<uuid:token>/', confirm_email, name='confirm_email'),
    path('email_confirmation_message/', email_confirmation_message, name='email_confirmation_message'),
]