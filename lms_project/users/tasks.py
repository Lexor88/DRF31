from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def deactivate_inactive_users():
    threshold_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=threshold_date)

    count = inactive_users.update(is_active=False)
    print(f"Деактивировано пользователей: {count}")