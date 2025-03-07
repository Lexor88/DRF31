from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwner, IsModerator
from .paginators import CoursePagination
from .tasks import send_course_update_email


@extend_schema(tags=["Courses"])
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    @extend_schema(summary="Получить список курсов", description="Возвращает все курсы, доступные пользователю.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Создать курс", description="Создаёт курс и привязывает его к текущему пользователю.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ("retrieve", "update", "partial_update"):
            self.permission_classes = [IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()

        # Проверяем время последнего обновления, если прошло меньше 4 часов — выходим
        if course.updated_at and timezone.now() - course.updated_at < timedelta(hours=4):
            return

        # Получаем подписчиков
        subscribers = Subscription.objects.filter(course=course).select_related('user')

        # Запускаем асинхронную отправку писем
        for subscription in subscribers:
            send_course_update_email.delay(subscription.user.email, course.name)

        # Обновляем время последнего обновления
        course.updated_at = timezone.now()
        course.save()


@extend_schema(tags=["Lessons"])
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Получить список уроков", description="Возвращает список всех уроков.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(tags=["Subscriptions"])
class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Подписка/отписка от курса",
        description="Позволяет пользователю подписаться или отписаться от курса.",
        request={"course_id": int},
        responses={200: {"message": "Подписка удалена"}, 201: {"message": "Подписка добавлена"}},
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.first().delete()
            return Response({"message": "Подписка удалена"}, status=200)
        else:
            Subscription.objects.create(user=user, course=course)
            return Response({"message": "Подписка добавлена"}, status=201)