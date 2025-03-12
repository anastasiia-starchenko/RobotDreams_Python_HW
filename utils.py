from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings

def send_activation_email(user):

    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    activation_url = f"{settings.SITE_URL}/activate/{uid}/{token}/"
    message = f"Перейдіть за посиланням, щоб активувати акаунт: {activation_url}"
    send_mail(
        "Активація акаунта",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )