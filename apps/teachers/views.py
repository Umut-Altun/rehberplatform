from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Teacher
from .forms import TeacherForm

def teacher_count_processor(request):
    """
    Toplam öğretmen sayısını template'lere gönderir
    """
    return {
        'total_teachers': Teacher.objects.count()
    } 

@login_required
def teachers_home(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'name')
    
    if query:
        if search_type == 'tc':
            teachers = Teacher.objects.filter(tc_no__icontains=query)
        else:  # name search
            teachers = Teacher.objects.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query)
            )
    else:
        teachers = Teacher.objects.all()[:20]  # Son 20 öğretmen
    
    context = {
        'active_page': 'teachers',
        'teachers': teachers,
        'query': query,
        'search_type': search_type
    }
    return render(request, 'teachers/teachers_home.html', context)

@login_required
def teacher_add(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'{teacher.first_name} {teacher.last_name} başarıyla eklendi.')
            return redirect('teachers:home')
    else:
        form = TeacherForm()
    
    context = {
        'active_page': 'teachers',
        'form': form,
        'title': 'Öğretmen Ekle'
    }
    return render(request, 'teachers/teacher_form.html', context)

@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            # Şifre değişikliği varsa güncelle
            if form.cleaned_data.get('password'):
                teacher.user.set_password(form.cleaned_data['password'])
                teacher.user.save()
            
            teacher = form.save()
            messages.success(request, f'{teacher.first_name} {teacher.last_name} başarıyla güncellendi.')
            return redirect('teachers:home')
    else:
        # Kullanıcı bilgilerini forma ekle
        initial_data = {
            'username': teacher.user.username if teacher.user else '',
        }
        form = TeacherForm(instance=teacher, initial=initial_data)
        # Şifre alanlarını formdan kaldır (düzenleme sırasında isteğe bağlı)
        form.fields['password'].required = False
        form.fields['password_confirm'].required = False
    
    context = {
        'active_page': 'teachers',
        'form': form,
        'teacher': teacher,
        'title': 'Öğretmen Düzenle'
    }
    return render(request, 'teachers/teacher_form.html', context)

@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        # Kullanıcıyı da sil
        if teacher.user:
            teacher.user.delete()
        teacher.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('teachers:home')
    
    context = {
        'active_page': 'teachers',
        'teacher': teacher
    }
    return render(request, 'teachers/teacher_confirm_delete.html', context)

@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    context = {
        'active_page': 'teachers',
        'teacher': teacher
    }
    return render(request, 'teachers/teacher_detail.html', context) 