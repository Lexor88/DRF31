# admin.py
from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    search_fields = ('name', 'owner__username')
    list_filter = ('owner',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'owner')
    search_fields = ('title', 'course__name', 'owner__username')
    list_filter = ('course', 'owner')
