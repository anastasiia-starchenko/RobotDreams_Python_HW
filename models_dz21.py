from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Grade(models.Model):
    value = models.IntegerField()
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.value}"

class Homework(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()


    def __str__(self):
        return self.title

class CustomUser(AbstractUser):

    pass

class YourModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)


class Rating(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Rating for {self.course.title} by {self.user.username}"


class Course(models.Model):
    title = models.CharField(max_length=255, default='Без назви')
    description = models.TextField(default='Без опису')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='Без опису')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Submission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"