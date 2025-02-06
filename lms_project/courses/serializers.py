from rest_framework import serializers
from .models import Course, Lesson
from django.contrib.auth import get_user_model

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Назначается автоматически
    moderators = serializers.SlugRelatedField(
        many=True,
        slug_field="username",
        queryset=User.objects.all(),
        required=False,
        default=list  # Безопасно добавляет пустой список, если не передан
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'owner', 'moderators']


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Назначается автоматически

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'owner']
