from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from .tasks import send_confirmation_email
from django.contrib import messages


def email_confirmation_message(request):
    return render(request, 'myapp/email_confirmation_message.html')

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('email_confirmation_message')
    else:
        form = RegisterForm()

    return render(request, 'myapp/register.html', {'form': form})

def confirm_email(request, token):
    user = get_object_or_404(User, confirmation_token=token)
    user.email_confirmed = True
    user.save()
    return HttpResponse("Ваш email підтверджено! Ви можете увійти в систему.")