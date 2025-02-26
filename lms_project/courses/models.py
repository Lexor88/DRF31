from django.db import models
from django.contrib.auth import get_user_model
from courses.validators import validate_link  # Импорт валидатора

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")  # Добавлено поле owner

    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


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
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_subscription')
        ]
