from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Course, Student


@shared_task
def send_confirmation_email(user_email, token):
    confirmation_link = f"http://127.0.0.1:8000/accounts/confirm/{token}/"
    message = f"Будь ласка, підтвердіть вашу реєстрацію: {confirmation_link}"

    send_mail(
        'Підтвердження реєстрації',
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )


@shared_task
def send_course_start_notification(course_id):
    course = Course.objects.get(id=course_id)
    students = Student.objects.filter(course=course)

    for student in students:
        send_mail(
            'Старт курсу!',
            f'Ваш курс "{course.title}" починається {course.start_date}.',
            settings.EMAIL_HOST_USER,
            [student.user.email],
            fail_silently=False,
        )


@shared_task
def send_homework_notification(student_email, assignment_name):
    send_mail(
        'Нове завдання',
        f'Вам доступне нове завдання: {assignment_name}.',
        settings.EMAIL_HOST_USER,
        [student_email],
        fail_silently=False,
    )


@shared_task
def send_homework_review_notification(student_email, assignment_name, grade):
    send_mail(
        'Перевірка ДЗ',
        f'Ваше завдання "{assignment_name}" перевірено. Ваша оцінка: {grade}.',
        settings.EMAIL_HOST_USER,
        [student_email],
        fail_silently=False,
    )