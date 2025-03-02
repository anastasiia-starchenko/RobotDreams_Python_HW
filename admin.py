from django.contrib import admin
from .models import Course, Student, Lecture, Assignment
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import Permission

admin.site.register(Permission)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Teacher').exists():
            return qs.filter(teacher=request.user)
        return qs

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Teacher').exists():
            return qs.filter(course__teacher=request.user)
        return qs

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Group)