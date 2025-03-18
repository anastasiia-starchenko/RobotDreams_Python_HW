from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_decode
from django.http import Http404
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Student, StudentPerformance
from .serializers import CourseSerializer, StudentSerializer, StudentPerformanceSerializer
from django.contrib.auth import authenticate, login
from myapp.models import CustomUser
from myapp.serializers import HomeworkSerializer
from rest_framework import serializers
from myapp.models import Lesson
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Homework
from .serializers import HomeworkSerializer


class CourseHomeworkListAPIView(APIView):
    def get(self, request, course_id):
        homeworks = Homework.objects.filter(course_id=course_id)
        serializer = HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Homework.objects.filter(lesson__course_id=course_id)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListAPIView(APIView):
    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)

        return redirect('success')
    return render(request, 'registration/register.html')
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmailAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('success_page')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def password_reset(request, uidb64, token):
    try:

        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        raise Http404("User not found")

    if default_token_generator.check_token(user, token):

        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                password_validation.validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
                return redirect('login')
        else:
            form = PasswordResetForm()
        return render(request, 'password_reset.html', {'form': form})
    else:
        raise Http404("Token is invalid or expired")

def home(request):
    return render(request, 'home.html')
def index(request):
    return render(request, 'index.html')

def registration_success(request):
    return render(request, 'myapp/registration_success.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Received username: {username}, password: {password}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("Invalid credentials")
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')

def success_view(request):
    return render(request, 'success.html')
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentPerformanceListAPIView(generics.ListAPIView):
    queryset = StudentPerformance.objects.all()
    serializer_class = StudentPerformanceSerializer
    permission_classes = [IsAuthenticated]


class SubmitHomeworkAPIView(generics.CreateAPIView):
    serializer_class = StudentPerformanceSerializer
    permission_classes = [IsAuthenticated]


class GradeHomeworkAPIView(generics.UpdateAPIView):
    queryset = StudentPerformance.objects.all()
    serializer_class = StudentPerformanceSerializer
    permission_classes = [IsAuthenticated]