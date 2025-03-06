from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.contrib.auth import get_user_model

def get_default_teacher():

    return get_user_model().objects.filter(is_staff=True).first()


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва курсу", default="Default Course Name")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=timezone.now)
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list, verbose_name="Теги")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курси"

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Студент")
    course = models.ForeignKey('Course', related_name='students', on_delete=models.CASCADE, verbose_name="Курс")
    points = models.IntegerField(default=0, verbose_name="Бали")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенти"

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class Teacher(models.Model):
    name = models.CharField(max_length=100, default='Default Name')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Викладач")
    bio = models.TextField(blank=True, verbose_name="Біографія")

    def __str__(self):
        return self.user.username