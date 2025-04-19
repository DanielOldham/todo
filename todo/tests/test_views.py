from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import Todo


class TestViews(TestCase):
    """
    Test suite for various todo application view functionalities.
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


    def test_edit_todo_authentication_redirect(self):
        """
        Test a user is redirected when attempting to edit a todo that does not belong to them.
        """

        user1 = User.objects.create_user(username='test1', password='password')
        user2 = User.objects.create_user(username='test2', password='password')
        self.client.login(username='test2', password='password')

        # todo belongs to user 1
        todo = Todo.objects.create(title='test', user=user1)

        # attempt to access edit todo page
        response = self.client.get(reverse('core:edit_todo_form', kwargs={'todo_id': todo.id}))

        # user should be redirected
        self.assertRedirects(response, reverse('core:todo_list'), status_code=302)


    def test_edit_todo_authentication(self):
        """
        Test a user is not redirected when attempting to edit a todo that they own.
        """

        user = User.objects.create_user(username='test', password='password')
        self.client.login(username='test', password='password')

        # todo belongs to user
        todo = Todo.objects.create(title='test', user=user)

        # attempt to access edit todo page
        response = self.client.get(reverse('core:edit_todo_form', kwargs={'todo_id': todo.id}))

        # user should be not be redirected
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_form.html')


    def test_delete_todo_authentication_redirect(self):
        """
        Test a user is redirected when attempting to delete a todo that does not belong to them.
        """

        user1 = User.objects.create_user(username='test1', password='password')
        user2 = User.objects.create_user(username='test2', password='password')
        self.client.login(username='test2', password='password')

        # todo belongs to user 1
        todo = Todo.objects.create(title='test', user=user1)

        # attempt to access delete todo page
        response = self.client.get(reverse('core:delete_todo', kwargs={'todo_id': todo.id}))

        # user should be redirected
        self.assertRedirects(response, reverse('core:todo_list'), status_code=302)


    def test_delete_todo_authentication(self):
        """
        Test a todo is deleted when user has permissions.
        """

        user = User.objects.create_user(username='test', password='password')
        self.client.login(username='test', password='password')

        # todo belongs to user
        todo = Todo.objects.create(title='test', user=user)

        # attempt to access delete todo page
        response = self.client.get(reverse('core:delete_todo', kwargs={'todo_id': todo.id}))

        # user should be redirected to list view
        self.assertRedirects(response, reverse('core:todo_list'), status_code=302)

        # todo should be deleted
        self.assertEqual(len(Todo.objects.all()), 0)