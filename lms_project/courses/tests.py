from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Course, Subscription

User = get_user_model()

class CourseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="testpass")
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(title="Test Course", owner=self.user)

    def test_create_course(self):
        response = self.client.post('/api/courses/', {'title': 'New Course'})
        self.assertEqual(response.status_code, 201)

    def test_subscription(self):
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Подписка добавлена")

        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Подписка удалена")
