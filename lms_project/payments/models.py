from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.id} - {self.status}'