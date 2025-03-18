from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, TodoForm
from django.contrib import auth
from .models import Todo


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
    Log out the current user.

    :param request: Django request
    :return: redirect to login page
    """

    auth.logout(request)
    return redirect('core:login')


@login_required
def todo_list(request):
    """
    Django view.
    Display the Todo List.

    :param request: Django request
    """
    todos = Todo.objects.filter(user=request.user)
    radio_input = request.GET.get('filter-options')

    # if radio_input, filter by pending or completed todos
    if radio_input:
        if radio_input == 'pending':
            todos = todos.filter(status='P')
        elif radio_input == 'completed':
            todos = todos.filter(status='C')

    # if there is keyword input, search for
    keyword_input = request.GET.get('keyword')
    if keyword_input:
        todos = todos.filter(notes__icontains=keyword_input).union(todos.filter(title__icontains=keyword_input))

    context = {'todos': todos}

    # create a filter message to display to the user
    filter_text = ''
    if radio_input != 'all' and keyword_input:
        filter_text = radio_input + ', \"' + keyword_input + '\"'
    elif radio_input != 'all':
        filter_text = radio_input
    elif keyword_input:
        filter_text = '\"' + keyword_input + '\"'

    context['filter_text'] = filter_text

    return render(request, 'todo_list.html', context=context)


@login_required
def change_todo_status(request, todo_id):
    """
    Django view.
    Swap the status of the given Todo object.

    :param request: Django request
    :todo_id: id of the Todo to update
    """

    # error handling
    try:
        todo = Todo.objects.get(id=todo_id)

        # if the todo doesn't belong to that user, raise exception
        if todo.user != request.user:
            raise PermissionDenied
    except (PermissionDenied, ObjectDoesNotExist):
        return redirect('core:todo_list')

    # flip status
    todo.status = 'C' if todo.status == 'P' else 'P'
    todo.save()
    return redirect('core:todo_list')


@login_required
def new_todo_form(request):
    """
    Django view.
    Display new Todo form and handle creation of new Todo.

    :param request: Django request
    """
    if request.method == 'GET':
        context = {'form': TodoForm(), 'form_type': 'add'}
        return render(request, 'todo_form.html', context)
    if request.method == 'POST':
        form = TodoForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('core:todo_list')
        else:
            # FIXME: send error message to todo list page
            return redirect('core:todo_list')


@login_required
def edit_todo_form(request, todo_id):
    """
    Django view.
    Display edit Todo form and handle editing of existing Todo objects.

    :param request: Django request
    :todo_id: id of the Todo to update
    """
    try:
        todo = Todo.objects.get(id=todo_id)

        # if the todo doesn't belong to that user, raise exception
        if todo.user != request.user:
            raise PermissionDenied

    except (ObjectDoesNotExist, PermissionDenied):
        return redirect('core:todo_list')

    if request.method == 'GET':
        context = {'form': TodoForm(instance=todo), 'form_type': 'edit'}
        return render(request, 'todo_form.html', context)

    if request.method == 'POST':
        form = TodoForm(data=request.POST, instance=todo)
        if form.is_valid():
            form.save()
        # FIXME: send error message to todo list page if form not valid

        return redirect('core:todo_list')


@login_required
def delete_todo(request, todo_id):
    """
    Django view.
    Delete a Todo object.

    :param request: Django request
    :todo_id: id of the Todo to delete
    """

    try:
        todo = Todo.objects.get(id=todo_id)

        # if the todo doesn't belong to that user, raise exception
        if todo.user != request.user:
            raise PermissionDenied

    except (ObjectDoesNotExist, PermissionDenied):
        return redirect('core:todo_list')

    todo.delete()
    return redirect('core:todo_list')
