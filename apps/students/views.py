from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm

def student_count_processor(request):
    """Context processor to add student count to all templates"""
    if not request.user.is_authenticated:
        return {'total_students': 0}
        
    if request.user.is_staff:
        # Staff kullanıcıları için tüm öğrencilerin sayısı
        total = Student.objects.count()
    elif hasattr(request.user, 'teacher_profile'):
        # Öğretmenler için sadece kendi öğrencilerinin sayısı
        total = Student.objects.filter(teacher=request.user.teacher_profile).count()
    else:
        total = 0
        
    return {
        'total_students': total
    }

@login_required
def students_home(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'name')
    
    # Başlangıç queryset'i
    if request.user.is_staff:
        # Staff kullanıcıları tüm öğrencileri görebilir
        students = Student.objects.all()
    elif hasattr(request.user, 'teacher_profile'):
        # Öğretmenler sadece kendi öğrencilerini görebilir
        students = Student.objects.filter(teacher=request.user.teacher_profile)
    else:
        # Diğer kullanıcılar için boş queryset
        students = Student.objects.none()
    
    # Arama filtreleri
    if query:
        if search_type == 'tc':
            students = students.filter(tc_no__icontains=query)
        else:  # name search
            students = students.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query)
            )
    else:
        # Arama yoksa son 20 öğrenciyi göster
        students = students[:20]
    
    context = {
        'active_page': 'students',
        'students': students,
        'query': query,
        'search_type': search_type
    }
    return render(request, 'students/students_home.html', context)

@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # Öğretmen kontrolü
            if hasattr(request.user, 'teacher_profile'):
                student.teacher = request.user.teacher_profile
            student.save()
            messages.success(request, f'{student.first_name} {student.last_name} başarıyla eklendi.')
            return redirect('students:home')
    else:
        form = StudentForm()
        
        # Öğretmen seçeneklerini filtrele
        if hasattr(request.user, 'teacher_profile'):
            # Eğer giriş yapan kullanıcı öğretmense, sadece kendisi görünsün
            form.fields['teacher'].queryset = form.fields['teacher'].queryset.filter(pk=request.user.teacher_profile.pk)
            form.fields['teacher'].initial = request.user.teacher_profile
            form.fields['teacher'].widget.attrs['disabled'] = 'disabled'
    
    context = {
        'active_page': 'students',
        'form': form,
        'title': 'Öğrenci Ekle'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Öğretmenler sadece kendi öğrencilerini düzenleyebilir
    if hasattr(request.user, 'teacher_profile') and student.teacher != request.user.teacher_profile:
        messages.error(request, 'Bu öğrenciyi düzenleme yetkiniz yok.')
        return redirect('students:home')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            # Öğretmen kontrolü
            if hasattr(request.user, 'teacher_profile'):
                student.teacher = request.user.teacher_profile
            
            # Şifre değişikliği varsa güncelle
            if form.cleaned_data.get('password'):
                student.user.set_password(form.cleaned_data['password'])
                student.user.save()
            
            student.save()
            messages.success(request, f'{student.first_name} {student.last_name} başarıyla güncellendi.')
            return redirect('students:home')
    else:
        initial_data = {
            'username': student.user.username if student.user else '',
        }
        form = StudentForm(instance=student, initial=initial_data)
        form.fields['password'].required = False
        form.fields['password_confirm'].required = False
        
        # Öğretmen seçeneklerini filtrele
        if hasattr(request.user, 'teacher_profile'):
            form.fields['teacher'].queryset = form.fields['teacher'].queryset.filter(pk=request.user.teacher_profile.pk)
            form.fields['teacher'].initial = request.user.teacher_profile
            form.fields['teacher'].widget.attrs['disabled'] = 'disabled'
    
    context = {
        'active_page': 'students',
        'form': form,
        'student': student,
        'title': 'Öğrenci Düzenle'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        # Kullanıcıyı da sil
        if student.user:
            student.user.delete()
        student.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('students:home')
    
    context = {
        'active_page': 'students',
        'student': student
    }
    return render(request, 'students/student_confirm_delete.html', context)

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {
        'active_page': 'students',
        'student': student
    }
    return render(request, 'students/student_detail.html', context)
