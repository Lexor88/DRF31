from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwnerOrReadOnly, IsModeratorReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorReadOnly | IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorReadOnly | IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
