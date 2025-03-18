from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import Todo


class TestViews(TestCase):
    """
    Test suite for various todo application views.
    Not exhaustive.
    """

    def test_authentication_required_redirect(self):
        """
        Test authentication required for the todo_list view.
        User should be redirected to login page if not authenticated.
        """

        # unauthenticated user should redirect
        response = self.client.get(reverse('core:todo_list'))
        self.assertEqual(response.status_code, 302)


    def test_authentication_required(self):
        """
        Test authentication required for the todo_list view.
        User should be able to access list view if authenticated.
        """

        User.objects.create_user(username='test', password='password')
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('core:todo_list'))

        # user should not be redirected
        self.assertEqual(response.status_code, 200)

        # template used should be list template
        self.assertTemplateUsed(response, 'todo_list.html')


    def test_todo_list_queryset(self):
        """
        Test the todo_list view context contains the correct Todo objects.
        """

        # create user, login user, create todos associated with user
        user= User.objects.create_user(username='test', password='password')
        self.client.login(username='test', password='password')
        Todo.objects.bulk_create([Todo(user=user, title='todo' + str(i)) for i in range(5)])

        # go to list
        response = self.client.get(reverse('core:todo_list'))

        # the todos from the context should be the same as all the ones in the test db
        self.assertQuerySetEqual(
            response.context['todos'],
            Todo.objects.all(),
            ordered=False
        )
