from django.shortcuts import render

def exercises_home(request):
    context = {
        'active_page': 'exercises'  # Menüde aktif sayfayı işaretlemek için
    }
    return render(request, 'exercises/exercises_home.html')
