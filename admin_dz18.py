from django.contrib import admin
from .models import Course, Student, Teacher, Tag, CourseTag, Enrollment, StudentPerformance
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'teacher')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'total_score')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CourseTagAdmin(admin.ModelAdmin):
    list_display = ('course', 'tag')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')

class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'score')


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CourseTag, CourseTagAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(StudentPerformance, StudentPerformanceAdmin)