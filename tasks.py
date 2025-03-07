from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_password_reset_email(email, uid, token):
    reset_url = f"http://localhost:8000/reset/{uid}/{token}/"
    send_mail(
        'Password Reset Request',
        f'Click the following link to reset your password: {reset_url}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )