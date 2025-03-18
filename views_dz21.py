from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import Course, Rating
from rest_framework import viewsets
from .models import Course, Rating, Assignment, Submission
from .serializers import CourseSerializer, RatingSerializer, AssignmentSerializer, SubmissionSerializer
from rest_framework.permissions import IsAuthenticated

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ви успішно зареєструвались!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('courses_list')
            else:
                messages.error(request, 'Невірний логін чи пароль')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})


def courses_list(request):
    if not request.user.is_authenticated:
        return redirect('login')


    courses = Course.objects.all()


    ratings = Rating.objects.filter(user=request.user)


    return render(request, 'myapp/courses_list.html', {
        'courses': courses,
        'ratings': ratings
    })