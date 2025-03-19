from django.urls import path
from myapp import views
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from myapp.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.contrib.auth import views as auth_views
from .views import register_view, registration_success_view
from .views import CourseHomeworkListAPIView, LessonListAPIView
from .views import SubmitHomeworkAPIView, GradeHomeworkAPIView
from .views import StudentPerformanceListAPIView, home

from .views import activate_account
from .views import success_view


urlpatterns = [

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('api/courses/<int:course_id>/homeworks/', CourseHomeworkListAPIView.as_view(), name='course-homeworks'),
    path('api/courses/', views.CourseListAPIView.as_view(), name='course-list'),
    path('api/students/', views.StudentListAPIView.as_view(), name='student-list'),
    path('api/student_performance/', views.StudentPerformanceListAPIView.as_view(), name='student-performance-list'),
    path('api/submit_homework/', views.SubmitHomeworkAPIView.as_view(), name='submit-homework'),
    path('api/grade_homework/<int:pk>/', views.GradeHomeworkAPIView.as_view(), name='grade-homework'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('success/', views.success_view, name='success'),
    path('registration_success/', registration_success_view, name='registration_success'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset'),
    path('reset/password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('admin/', admin.site.urls),
    path('homework/<int:lesson_id>/submit/', SubmitHomeworkAPIView.as_view(), name='homework-submit'),
    path('homework/<int:homework_id>/review/', GradeHomeworkAPIView.as_view(), name='homework-review'),
    path('grade_homework/', GradeHomeworkAPIView.as_view(), name='grade-homework'),
    path('courses/', views.CourseListAPIView.as_view(), name='courses-list'),
]