from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('submit-error/', views.submit_error_report, name='submit_error'),
    # Eğer formu AJAX ile yüklemek için ayrı bir view kullanırsanız:
    # path('get-form/', views.get_error_report_form, name='get_form'),
] 