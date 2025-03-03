from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.course_list, name='course-list'),
    path('<int:course_id>/', views.course_detail, name='course-detail'),
]