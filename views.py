from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Головна сторінка
def home(request):
    return render(request, 'home.html')

# Сторінка реєстрації
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна!')
            return redirect('home')
        else:
            messages.error(request, 'Виникла помилка при реєстрації.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Сторінка логіну
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вхід виконано успішно!')
            return redirect('home')
        else:
            messages.error(request, 'Невірні дані для входу.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Логаут
def user_logout(request):
    logout(request)
    messages.success(request, 'Ви вийшли із системи.')
    return redirect('home')