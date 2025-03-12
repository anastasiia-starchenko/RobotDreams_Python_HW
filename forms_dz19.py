from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField()

    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            user = get_user_model().objects.get(email=email)
            self.cleaned_data['username'] = user.username
            return user.username
        except get_user_model().DoesNotExist:
            raise forms.ValidationError("Цей email не зареєстровано.")

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name']


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']