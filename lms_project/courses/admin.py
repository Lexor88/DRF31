from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')  # Заменяем 'title' на 'name'
    search_fields = ('name', 'owner__username')  # Аналогично в search_fields
    list_filter = ('owner',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'owner')  # Заменить 'name' на 'title'
    search_fields = ('title', 'course__name', 'owner__username')  # 'course__title' -> 'course__name'
    list_filter = ('course', 'owner')