from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib import auth


def login(request):
    """
    Django view.
    Display login page to user.

    :param request: Django request
    :return: rendered login template if request is GET (or if there are errors), else returns redirect to to_do list view
    """

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('core:todo_list')
        else:
            # errors logging in
            return render(request, 'login.html', {'form': form})

def signup(request):
    """
    Django view.
    Display signup page.

    :param request: Django request
    :return: rendered signup template if request is GET (or there are errors), else return redirect to dashboard view
    """

    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('core:todo_list')
        else:
            # user is not created
            return render(request, 'signup.html', {'form': form})


def logout_user(request):
    """
    Django view.
    Logout the current user.

    :param request: Django request
    :return: redirect to login
    """

    auth.logout(request)
    return redirect('core:login')

@login_required
def todo_list(request):
    return render(request, 'todo_list.html')