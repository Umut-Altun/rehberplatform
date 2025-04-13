from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teachers_home, name='home'),
    path('add/', views.teacher_add, name='add'),
    path('<int:pk>/edit/', views.teacher_edit, name='edit'),
    path('<int:pk>/delete/', views.teacher_delete, name='delete'),
    path('<int:pk>/detail/', views.teacher_detail, name='detail'),
] 