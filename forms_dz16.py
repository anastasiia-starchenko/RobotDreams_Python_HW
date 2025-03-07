from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Course


class CourseRegistrationForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Оберіть курс")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)