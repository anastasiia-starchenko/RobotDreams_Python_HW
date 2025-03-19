from django.urls import path
from .views import CourseListView, StudentListView, register, update_profile, CourseDetailView
from .views import register_course

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:course_id>/students/', StudentListView.as_view(), name='student_list'),
    path('register/', register, name='register'),
    path('update_profile/', update_profile, name='update_profile'),
    path('register_course/', register_course, name='register_course'),
]