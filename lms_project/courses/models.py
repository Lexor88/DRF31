from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_courses")
    moderators = models.ManyToManyField(User, related_name="moderated_courses", blank=True)  # Добавляем модераторов

    objects = models.Manager()  # Явный менеджер

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")

    objects = models.Manager()  # Явный менеджер

    def __str__(self):
        return self.title
