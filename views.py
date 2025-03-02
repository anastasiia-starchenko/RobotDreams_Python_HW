from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Course

def home(request):
    return render(request, 'myapp/home.html')

def course_list(request):
    courses = Course.objects.all()
    course_data = [{'id': course.id, 'title': course.title, 'description': course.description} for course in courses]
    return JsonResponse(course_data, safe=False)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lectures = [{'title': lecture.title, 'content': lecture.content} for lecture in course.lectures.all()]
    assignments = [{'title': assignment.title, 'description': assignment.description, 'due_date': assignment.due_date}
                   for assignment in course.assignments.all()]
    students = [{'name': student.name, 'email': student.email} for student in course.students.all()]

    course_data = {
        'title': course.title,
        'description': course.description,
        'lectures': lectures,
        'assignments': assignments,
        'students': students
    }
    return JsonResponse(course_data)