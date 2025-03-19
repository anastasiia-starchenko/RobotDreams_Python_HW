from rest_framework import serializers
from .models import Course, Student, StudentPerformance
from myapp.models import Homework


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'start_date', 'description', 'teacher']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'course', 'total_score', 'full_name', 'email']

class StudentPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPerformance
        fields = ['id', 'student', 'course', 'score']