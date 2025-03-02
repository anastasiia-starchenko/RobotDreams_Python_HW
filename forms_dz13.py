from django import forms
from .models import Course, Lecture

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['course', 'title', 'content']