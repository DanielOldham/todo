from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Todo


class SignupForm(UserCreationForm):
    """
    Django UserCreationForm.
    Sets up user creation form and adds CSS bootstrap classes and HTML placeholders.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # loop through fields and adds a bootstrap form-control class
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['username'].widget.attrs.update({'placeholder': 'type your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'type your email'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'type your first name'}, required=True)
        self.fields['last_name'].widget.attrs.update({'placeholder': 'type your last name'}, required=True)
        self.fields['password1'].widget.attrs.update({'placeholder': 'type your password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'confirm your password'})

    class Meta:
        """
        Django Meta inner class.
        """
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    """
    Django AuthenticationForm.
    Sets up authentication form and adds CSS bootstrap classes and HTML placeholders.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # loop through fields and adds a bootstrap form-control class
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['username'].widget.attrs.update({'placeholder': 'type your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'type your password'})

    class Meta:
        model = User
        fields = ['username', 'password']


class TodoForm(forms.ModelForm):
    """
    Django ModelForm.
    Allows creation and modification of a Todo.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # loop through fields and adds a bootstrap form-control class
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['title'].widget.attrs.update({'placeholder': 'My New Todo'}, required=True)
        self.fields['notes'].widget.attrs.update({'placeholder': 'My New Todo Notes (optional)'})

    class Meta:
        """
        Django Meta inner class.
        """
        model=Todo
        fields=['title', 'notes']