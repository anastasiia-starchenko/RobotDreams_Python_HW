from django.urls import path
from myapp import views
from .views import CourseHomeworkListAPIView, LessonListAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('api/courses/<int:course_id>/homeworks/', CourseHomeworkListAPIView.as_view(), name='course-homeworks'),
    path('api/courses/', views.CourseListAPIView.as_view(), name='course-list'),
    path('api/students/', views.StudentListAPIView.as_view(), name='student-list'),
    path('api/student_performance/', views.StudentPerformanceListAPIView.as_view(), name='student-performance-list'),
    path('api/submit_homework/', views.SubmitHomeworkAPIView.as_view(), name='submit-homework'),
    path('api/grade_homework/<int:pk>/', views.GradeHomeworkAPIView.as_view(), name='grade-homework'),
    path('success/', views.success_view, name='success'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('reset/<uidb64>/<token>/', views.password_reset, name='password_reset'),
]