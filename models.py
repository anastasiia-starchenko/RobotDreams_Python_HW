from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        if not username:
            raise ValueError("Username field is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, default='Anonymous')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.email})"


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="courses")
    start_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    total_score = models.IntegerField(default=0)
    full_name = models.CharField(max_length=100, default='Anonymous')

    def __str__(self):
        return self.user.username if self.user else "No User"


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Homework(models.Model):
    content = models.TextField(verbose_name="Контент", default="")
    created_at = models.DateTimeField(default=timezone.now)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Домашнє завдання'
        verbose_name_plural = 'Домашні завдання'

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

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


class Rating(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name="Оцінка", default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'

    def __str__(self):
        return f"Оцінка студента {self.student}"


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField(default="")
    grade = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Submission for {self.assignment.title} by {self.student.username}'



class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date_assigned = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.user.username} - {self.course.name}: {self.grade}'

    def get_grade_letter(self):
        if self.grade is not None:
            if self.grade >= 90:
                return 'A'
            elif self.grade >= 80:
                return 'B'
            elif self.grade >= 70:
                return 'C'
            elif self.grade >= 60:
                return 'D'
            else:
                return 'F'
        return 'N/A'