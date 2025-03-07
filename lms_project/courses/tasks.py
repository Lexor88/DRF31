from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(user_email, course_title):
    send_mail(
        subject=f'Обновление курса: {course_title}',
        message=f'Здравствуйте! В курсе "{course_title}" появились новые материалы.',
        from_email='noreply@example.com',
        recipient_list=[user_email],
    )