from django.contrib.auth.models import User
from django.test import TestCase
from core.forms import SignupForm, LoginForm, TodoForm


class TestForms(TestCase):
    """
    Test suite for todo application forms.
    """

    def test_invalid_signup_form(self):
        """
        Test SignupForm validation with invalid data.
        """

        form = SignupForm(data={
            'username': '',
            'email': 'bad email',
            'password1': 'asdf',
            'password2': 'different_password123',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'email': ['Enter a valid email address.'],
            'password2': ['The two password fields didn’t match.'],
        })


    def test_valid_signup_form(self):
        """
        Test SignupForm validation with valid data.
        """

        form = SignupForm(data={
            'username': 'test',
            'email': 'good@email.com',
            'password1': 'asdfasdf123',
            'password2': 'asdfasdf123',
        })

        self.assertTrue(form.is_valid())


    def test_invalid_login_form(self):
        """
        Test LoginForm validation with invalid data.
        """

        form = LoginForm(data={
            'username': '',
            'password': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
        })


    def test_valid_login_form(self):
        """
        Test LoginForm validation with valid data.
        """

        User.objects.create_user(username='test', password='password')
        form = LoginForm(data={
            'username': 'test',
            'password': 'password',
        })
        self.assertTrue(form.is_valid())


    def test_invalid_todo_form(self):
        """
        Test TodoForm validation with invalid data.
        """

        form = TodoForm(data={
            'title': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'title': ['This field is required.'],
        })


    def test_valid_todo_form(self):
        """
        Test TodoForm validation with valid data.
        """

        form = TodoForm(data={
            'title': 'test',
            'notes': 'test notes',
        })
        self.assertTrue(form.is_valid())
