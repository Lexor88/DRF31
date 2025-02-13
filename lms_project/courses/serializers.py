from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)  # Используем вычисляемое поле

    class Meta:
        model = Course
        fields = ['id', 'title', 'owner', 'moderators', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return obj.subscriptions.filter(user=user).exists()  # Проверка, подписан ли пользователь

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user  # Устанавливаем владельца
        return super().create(validated_data)



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'owner', 'video_link']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user  # Устанавливаем владельца
        return super().create(validated_data)
