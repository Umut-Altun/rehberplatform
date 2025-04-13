from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    path('', views.exercises_home, name='home'),
]
