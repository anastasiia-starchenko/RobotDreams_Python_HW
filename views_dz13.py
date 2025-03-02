from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Lecture
from .forms import CourseForm, LectureForm

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'myapp/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'myapp/course_detail.html', {'course': course})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'myapp/add_course.html', {'form': form})


def add_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = LectureForm()
    return render(request, 'myapp/add_lecture.html', {'form': form})