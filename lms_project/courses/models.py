from django.db import models
from django.contrib.auth import get_user_model
from courses.validators import validate_link  # Импорт валидатора

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_courses")
    moderators = models.ManyToManyField(User, related_name="moderated_courses", blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")
    video_link = models.URLField(blank=True, null=True, validators=[validate_link])  # Подключение валидатора

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions")

    class Meta:
        unique_together = ('user', 'course')
