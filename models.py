from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings


def get_default_teacher():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.filter(is_staff=True).first()


class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4, unique=True)


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=get_default_teacher,
        verbose_name="Викладач"
    )

    def __str__(self):
        return self.title