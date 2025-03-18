from django.contrib.auth.models import User
from django.test import TestCase
from core.models import Todo


class TestModels(TestCase):
    """
    Test suite for todo application models.
    """

    def setUp(self):
        User.objects.create_user(username='test', password='password')

    def test_create_todo_model(self):
        user = User.objects.get(username='test')
        instance = Todo.objects.create(title="New To-do", user=user)

        self.assertEqual(instance.title, 'New To-do')
        self.assertEqual(instance.user, user)
        self.assertEqual(instance.status, 'P')
