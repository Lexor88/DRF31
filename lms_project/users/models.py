from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Кастомная модель пользователя с уникальным email."""
    email = models.EmailField(unique=True)

    def is_moderator(self):
        """Проверка: является ли пользователь модератором."""
        return self.groups.filter(name="moderators").exists()
