from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, RatingViewSet, AssignmentViewSet, SubmissionViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse



router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path("", lambda request: JsonResponse({"message": "API is running"})),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('courses/', views.courses_list, name='courses_list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
Footer
