from django.contrib import admin
from .models import Course, Student, CustomUser, Teacher

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profile_picture')


admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)