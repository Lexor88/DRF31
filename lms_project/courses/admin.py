from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')  # Отображение в списке
    search_fields = ('title', 'owner__username')  # Поиск по названию курса и владельцу
    list_filter = ('owner',)  # Фильтр по владельцу


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'owner')
    search_fields = ('title', 'course__title', 'owner__username')
    list_filter = ('course', 'owner')
