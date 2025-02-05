from rest_framework import serializers
from .models import Course, Lesson
from django.contrib.auth import get_user_model

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    moderators = serializers.SlugRelatedField(
        many=True,
        slug_field="username",
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'owner', 'moderators']


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'owner']
