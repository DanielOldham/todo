import json
from datastar_py.sse import ServerSentEventGenerator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse
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


@login_required
def logout_user(request):
    """
    Django view.
    Log out the current user.

    :param request: Django request
    :return: redirect to login page
    """
    auth.logout(request)
    return redirect('core:login')


def about(request):
    return render(request, 'about.html')


@login_required
def todo_list(request):
    """
    Django view.
    Display the Todo List.

    :param request: Django request
    :return: rendered todo_list template
    """
    todos = Todo.objects.filter(user=request.user).order_by('title')

    page = 1
    keyword_input = ""
    status_input = ""
    try:
        qdict = json.loads(request.GET.get("datastar", "{}"))
        page = int(qdict.get("page", 1)) if qdict.get("page") else 1
        keyword_input = qdict.get("keyword", "")
        status_input = qdict.get("status", "")
    except TypeError:
        pass

    # if there is todo status input, filter by pending or completed todos
    if status_input:
        if status_input == 'pending':
            todos = todos.filter(status='P')
        elif status_input == 'completed':
            todos = todos.filter(status='C')

    # if there is keyword input, search for keyword in title and notes
    if keyword_input:
        todos = todos.filter(notes__icontains=keyword_input).union(todos.filter(title__icontains=keyword_input))

    # pagination
    paginator = Paginator(todos, 10)
    todo_paginator = paginator.get_page(page)
    context = {'todos': todo_paginator}

    # return datastar requests as server sent events
    if "datastar" in request.GET:
        # render only list template partial
        html_response = render(
            request, "todo_list.html#todo_list_card", context=context
        )

        # merge rendered template partial with the rest of the template
        sse_response = ServerSentEventGenerator.merge_fragments(
            html_response.content.decode("utf-8").splitlines()
        )
        response = HttpResponse(sse_response)
        response["Content-Type"] = "text/event-stream"
        response["Cache-Control"] = "no-cache"
        return response

    # not a datastar request, return regular render
    return render(request, 'todo_list.html', context=context)


@login_required
def change_todo_status(request, todo_id):
    """
    Django view.
    Swap the status of the given Todo object.

    :param request: Django request
    :param todo_id: id of the Todo to update
    :return: redirect to list view
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
    :return: redirect to list view
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
    :param todo_id: id of the Todo to update
    :return: rendered todo_form template if permissions valid, otherwise redirects to list view
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
    :param todo_id: id of the Todo to delete
    :return: redirect to list view
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