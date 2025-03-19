from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import Course, Rating, Homework, Lesson, Student
from rest_framework import viewsets
from .models import Assignment, Submission
from .serializers import CourseSerializer, RatingSerializer, AssignmentSerializer, SubmissionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from myapp.serializers import HomeworkSerializer, LessonSerializer
from rest_framework import generics
from .serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model


def home(request):
    return HttpResponse("Ласкаво просимо на головну сторінку!")

class StudentPerformanceListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Ваша логіка тут
        return Response({"message": "Привіт, ось список студентських результатів!"})
class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Course.objects.filter(students=user)
        return Course.objects.all()

class LessonListAPIView(ListAPIView):
    """
    API для отримання списку уроків.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.all()

class CourseHomeworkListAPIView(ListAPIView):
    """
    API-представлення для отримання списку домашніх завдань до курсу.
    """
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        user = self.request.user
        if course_id:
            course = Course.objects.get(id=course_id)
            if user.role == 'student' and user in course.students.all():
                return Homework.objects.filter(lesson__course_id=course_id, student__user=user)
            elif user.role == 'teacher' and course.teacher.user == user:
                return Homework.objects.filter(lesson__course_id=course_id)
        return Homework.objects.none()

class SubmitHomeworkAPIView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class GradeHomeworkAPIView(generics.UpdateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(assignment__course__teacher__user=self.request.user)


def registration_success_view(request):
    return render(request, 'registration_success.html')

def register_view(request):
    return register_view(request)

class CustomTokenObtainPairView(TokenObtainPairView):
    pass


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


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Акаунт успішно активовано!")
        else:
            return HttpResponse("Невірне посилання активації.")
    except Exception as e:
        return HttpResponse(f"Сталася помилка: {e}")

def success_view(request):
    return HttpResponse("Успіх! Операція пройшла успішно.")