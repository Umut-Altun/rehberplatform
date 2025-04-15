from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def exercises_home(request):
    context = {
        'active_page': 'exercises'  # Menüde aktif sayfayı işaretlemek için
    }
    return render(request, 'exercises/exercises_home.html')
