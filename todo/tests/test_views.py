from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.views import *

class TestViews(TestCase):
    def test_authentication_required(self):
        # Unauthenticated user
        response = self.client.get(reverse('core:todo_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Authenticated user
        User.objects.create_user(username='test', password='password')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('core:todo_list'))
        self.assertEqual(response.status_code, 200)
