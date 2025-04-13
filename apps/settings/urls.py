from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_home, name='home'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('settings/update/', views.update_settings, name='update_settings'),
    path('password/change/', views.change_password, name='change_password'),
]
