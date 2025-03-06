from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import Course, Student
from .filters import CourseFilter, StudentFilter
from .forms import UserProfileForm, RegisterForm, CourseRegistrationForm



User = get_user_model()

def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/list.html', {'courses': courses})


def register_course(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']


            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Користувач із таким email уже існує.')
            else:
                form.save()
                return redirect('course_list')

    else:
        form = CourseRegistrationForm()

    return render(request, 'courses/register.html', {'form': form})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'myapp/course_detail.html'
    context_object_name = 'course'

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        student = Student(user=request.user, course=course)
        student.save()
        return redirect('course_detail', pk=course.pk)


def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'myapp/update_profile.html', {'form': form})


class CourseListView(ListView):
    model = Course
    template_name = 'myapp/courses_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = Course.objects.all()
        self.filterset = CourseFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class StudentListView(ListView):
    model = Student
    template_name = 'myapp/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        queryset = Student.objects.filter(course=course)
        self.filterset = StudentFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['course'] = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return context


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('course_list')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})