from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionView

app_name = "courses"

# Создаем маршрутизатор и регистрируем наши вьюсеты
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),  # Регистрация маршрутов для Course и Lesson
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),  # Подписка на курс
]
