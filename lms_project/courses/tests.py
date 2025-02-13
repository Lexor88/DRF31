from django.test import TestCase
from .models import Lesson, Course, Subscription
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .validators import validate_link

from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class LessonValidatorTests(TestCase):
    def test_lesson_creation_with_invalid_link(self):
        user = User.objects.create_user(username="testuser", password="password", email="testuser@example.com")
        course = Course.objects.create(title="Test Course", owner=user)

        invalid_link = "https://example.com"
        with self.assertRaises(ValidationError):
            validate_link(invalid_link)

        lesson = Lesson(
            title="Test Lesson",
            course=course,
            owner=user,
            video_link=invalid_link
        )
        with self.assertRaises(ValidationError):
            lesson.full_clean()

    def test_lesson_creation_with_valid_link(self):
        user = User.objects.create_user(username="testuser", password="password", email="testuser@example.com")
        course = Course.objects.create(title="Test Course", owner=user)

        valid_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        try:
            validate_link(valid_link)
        except ValidationError:
            self.fail("ValidationError raised for a valid YouTube link")

        lesson = Lesson(
            title="Test Lesson",
            course=course,
            owner=user,
            video_link=valid_link
        )
        try:
            lesson.full_clean()
        except ValidationError:
            self.fail("ValidationError raised for a valid Lesson instance")


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password", email="testuser@example.com")
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_add_subscription(self):
        response = self.client.post('/api/courses/subscribe/', {'course_id': self.course.id})
        print(response.data)  # Вывод данных ошибки
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post('/api/courses/subscribe/', {'course_id': self.course.id})
        print(response.data)  # Вывод данных ошибки
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка удалена')


class CourseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password", email="testuser@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        data = {"title": "Test Course"}
        response = self.client.post("/api/courses/courses/", data, format="json")
        print(response.data)  # Вывод данных ошибки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

    def test_get_course(self):
        course = Course.objects.create(title="Test Course", owner=self.user)
        response = self.client.get(f"/api/courses/courses/{course.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Course")

    def test_update_course(self):
        course = Course.objects.create(title="Test Course", owner=self.user)
        data = {"title": "Updated Course"}
        response = self.client.patch(f"/api/courses/courses/{course.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=course.id).title, "Updated Course")

    def test_delete_course(self):
        course = Course.objects.create(title="Test Course", owner=self.user)
        response = self.client.delete(f"/api/courses/courses/{course.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_create_lesson(self):
        course = Course.objects.create(title="Test Course", owner=self.user)
        data = {"title": "Test Lesson", "course": course.id}
        response = self.client.post("/api/courses/lessons/", data, format="json")
        print(response.data)  # Вывод данных ошибки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)


class LessonTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password", email="owner@example.com")
        self.client.force_authenticate(user=self.owner)
        self.course = Course.objects.create(title="Owned Course", owner=self.owner)

    def test_create_lesson(self):
        data = {"title": "Test Lesson", "course": self.course.id}
        response = self.client.post("/api/courses/lessons/", data)
        print(response.data)  # Вывод данных ошибки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)


class PermissionTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password", email="owner@example.com")
        self.other_user = User.objects.create_user(username="other", password="password", email="other@example.com")
        self.course = Course.objects.create(title="Owned Course", owner=self.owner)

    def test_owner_can_update_course(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(f"/api/courses/courses/{self.course.id}/", {"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update_course(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(f"/api/courses/courses/{self.course.id}/", {"title": "Updated"})
        print(response.data)  # Вывод данных ошибки
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
