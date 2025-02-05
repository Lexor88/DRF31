from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson

class Command(BaseCommand):
    help = "Создать группу модераторов с правами на редактирование курсов и уроков"

    def handle(self, *args, **kwargs):
        moderators, created = Group.objects.get_or_create(name="moderators")

        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct],
            codename__in=["change_course", "change_lesson"]
        )

        moderators.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Группа "Модераторы" создана!'))
