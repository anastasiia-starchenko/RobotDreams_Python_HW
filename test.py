from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from .models import Course, Homework, Lesson, Tag, Teacher

User = get_user_model()

class APITestSuite(APITestCase):
    def setUp(self):

        self.student = User.objects.create_user(username="student", password="password", email="student@example.com")
        self.teacher_user = User.objects.create_user(username="teacher", password="password", email="teacher@example.com")
        self.teacher_user.role = 'teacher'
        self.teacher_user.save()


        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")


        self.admin = User.objects.create_superuser(username="admin", password="password", email="admin@example.com")


        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(days=30)
        self.course = Course.objects.create(
            title="Python Basics",
            name="Python Basics",
            teacher=self.teacher,
            start_date=self.start_date,
            end_date=self.end_date
        )
        self.lesson = Lesson.objects.create(title="Lesson 1", description="This is a test lesson")
        self.homework = Homework.objects.create(lesson=self.lesson, content="My Homework")


        self.python_tag = Tag.objects.create(name="Python")
        self.django_tag = Tag.objects.create(name="Django")


        self.course.tags.create(tag=self.python_tag)
        self.course.tags.create(tag=self.django_tag)


        self.courses_url = reverse("courses-list")
        self.homework_submit_url = reverse("homework-submit", args=[self.lesson.id])
        self.homework_review_url = reverse("homework-review", args=[self.homework.id])


        self.assertIsNotNone(self.student)
        self.assertIsNotNone(self.teacher_user)
        self.assertIsNotNone(self.admin)

    def test_get_courses_as_student(self):
        """Перевірка, що студент може отримати список своїх курсів"""
        self.client.login(username="student", password="password")
        response = self.client.get(self.courses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, str(response.data))

    def test_get_courses_as_teacher(self):
        """Перевірка, що викладач може отримати список курсів, які він веде"""
        self.client.login(username="teacher", password="password")
        response = self.client.get(self.courses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, str(response.data))

    def test_student_submit_homework(self):
        """Перевірка здачі домашнього завдання студентом"""
        self.client.login(username="student", password="password")
        data = {"content": "New Homework Submission"}
        response = self.client.post(self.homework_submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_submit_homework(self):
        """Перевірка, що викладач не може здати домашнє завдання"""
        self.client.login(username="teacher", password="password")
        data = {"content": "Teacher Homework Submission"}
        response = self.client.post(self.homework_submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_review_homework(self):
        """Перевірка, що викладач може оцінити домашку студента"""
        self.client.login(username="teacher", password="password")
        data = {"grade": 10, "feedback": "Good job!"}
        response = self.client.post(self.homework_review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_review_homework(self):
        """Перевірка, що студент не може перевіряти домашки"""
        self.client.login(username="student", password="password")
        data = {"grade": 10, "feedback": "Nice work!"}
        response = self.client.post(self.homework_review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_access_to_all_courses(self):
        """Перевірка, що адміністратор має доступ до всіх курсів"""
        self.client.login(username="admin", password="password")
        response = self.client.get(self.courses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, str(response.data))

    def test_student_cannot_access_other_students_homework(self):
        """Перевірка, що студент не може переглядати домашнє завдання інших студентів"""
        another_homework = Homework.objects.create(lesson=self.lesson, content="Another Homework")
        self.client.login(username="student", password="password")
        response = self.client.get(reverse("homework-detail", args=[another_homework.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_access_to_homework(self):
        """Перевірка, що викладач може бачити домашнє завдання студента"""
        self.client.login(username="teacher", password="password")
        response = self.client.get(reverse("homework-detail", args=[self.homework.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.homework.content, str(response.data))


    def test_filter_courses_by_teacher(self):
        """Перевірка фільтрації курсів за викладачем"""
        self.client.login(username="student", password="password")
        response = self.client.get(self.courses_url, {"teacher": self.teacher.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, str(response.data))

    def test_filter_courses_by_tags(self):
        """Перевірка фільтрації курсів за тегами"""
        self.client.login(username="student", password="password")
        response = self.client.get(self.courses_url, {"tags": self.python_tag.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, str(response.data))


    def test_filter_courses_by_start_date(self):
        """Перевірка фільтрації курсів за датою старту"""
        self.client.login(username="student", password="password")
        response = self.client.get(self.courses_url, {"start_date": self.course.start_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, str(response.data))


    def test_filter_courses_with_multiple_tags(self):
        """Перевірка фільтрації курсів з кількома тегами"""
        self.course.tags.create(tag=self.django_tag)
        self.client.login(username="student", password="password")
        response = self.client.get(self.courses_url, {"tags": [self.python_tag.id, self.django_tag.id]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, str(response.data))