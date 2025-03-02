from django.contrib import admin
from .models import Course, Assignment, Submission

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('course', 'due_date')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'grade')
    search_fields = ('student__username', 'assignment__title')
    list_filter = ('assignment', 'submitted_at', 'grade')

admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)