from django.contrib import admin
from .models import Course, Student, Lecture, Assignment

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Lecture)
admin.site.register(Assignment)