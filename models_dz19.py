from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class Homework(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Homework by {self.student} for {self.lesson}"

def get_default_teacher():
    teacher = Teacher.objects.first()
    if teacher:
        return teacher
    return None

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=get_default_teacher)
    end_date = models.DateField()

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    full_name = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField(default='example@example.com')

    def __str__(self):
        return self.user.username


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CourseTag(models.Model):
    course = models.ForeignKey(Course, related_name="tags", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name="courses", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title} - {self.tag.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"


class StudentPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}: {self.score}"