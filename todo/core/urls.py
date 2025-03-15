from . import views
from django.urls import path

app_name = 'core'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.todo_list, name='todo_list'),
    path('todo/add', views.new_todo_form, name='new_todo_form'),
    path('todo/edit/<int:todo_id>', views.edit_todo_form, name='edit_todo_form'),
    path('todo/delete/<int:todo_id>', views.delete_todo, name='delete_todo'),
    path('todo/status/<int:todo_id>', views.change_todo_status, name='change_todo_status'),
]
