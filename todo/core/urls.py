from . import views
from django.urls import path

app_name = 'core'
urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
