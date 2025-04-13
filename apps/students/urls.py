from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.students_home, name='home'),
    path('add/', views.student_add, name='add'),
    path('<int:pk>/edit/', views.student_edit, name='edit'),
    path('<int:pk>/delete/', views.student_delete, name='delete'),
    path('<int:pk>/detail/', views.student_detail, name='detail'),
]
