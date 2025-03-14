from . import views
from django.urls import path

app_name = 'core'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.todo_list, name='todo_list')
]
