from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm
import pandas as pd
import io
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def student_count_processor(request):
    """Öğrenci sayısını tüm şablonlara eklemek için bağlam işlemcisi"""
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
        students = Student.objects.all()
    elif hasattr(request.user, 'teacher_profile'):
        students = Student.objects.filter(teacher=request.user.teacher_profile)
    else:
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
            try:
                # Önce User nesnesini oluştur
                user_data = {
                    'username': form.cleaned_data.get('username'),
                    'password': form.cleaned_data.get('password'),
                    'email': form.cleaned_data.get('email'),
                    'first_name': form.cleaned_data.get('first_name'),
                    'last_name': form.cleaned_data.get('last_name'),
                }
                user = User.objects.create_user(**user_data)
                
                # Sonra Student nesnesini oluştur
                student = form.save(commit=False)
                student.user = user  # User nesnesini Student'a bağla
                if hasattr(request.user, 'teacher_profile'):
                    student.teacher = request.user.teacher_profile
                student.save()
                
                messages.success(request, f'{student.first_name} {student.last_name} başarıyla eklendi.')
                return redirect('students:home')
            except Exception as e:
                # Hata durumunda oluşturulan user'ı sil
                if 'user' in locals():
                    user.delete()
                messages.error(request, f'Öğrenci eklenirken bir hata oluştu: {str(e)}')
        else:
            messages.error(request, 'Lütfen formdaki hataları düzeltin.')
    else:
        form = StudentForm()
        
        # Öğretmen seçeneklerini filtrele
        if hasattr(request.user, 'teacher_profile'):
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

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student, edit_mode=True)
        
        if form.is_valid():
            try:
                student = form.save(commit=False)
                if hasattr(request.user, 'teacher_profile'):
                    student.teacher = request.user.teacher_profile
                student.save()
                
                messages.success(request, f'{student.first_name} {student.last_name} başarıyla güncellendi.')
                return redirect('students:home')
            except Exception as e:
                messages.error(request, f'Öğrenci güncellenirken bir hata oluştu: {str(e)}')
        else:
            messages.error(request, 'Lütfen formdaki hataları düzeltin.')
    else:
        form = StudentForm(instance=student, edit_mode=True)
    
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
        try:
            student_name = f'{student.first_name} {student.last_name}'
            if student.user:
                student.user.delete()
            student.delete()
            messages.success(request, f'{student_name} başarıyla silindi.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f'{student_name} başarıyla silindi.'})
            return redirect('students:home')
        except Exception as e:
            messages.error(request, f'Öğrenci silinirken bir hata oluştu: {str(e)}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)})
            return redirect('students:home')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {
        'active_page': 'students',
        'student': student
    }
    return render(request, 'students/student_detail.html', context)

@login_required
def download_excel_template(request):
    """Excel şablonunu indir"""
    # Şablon sütunları
    columns = [
        'Kullanıcı Adı*', 'Şifre*', 'Ad*', 'Soyad*', 
        'TC Kimlik No*', 'Okul No*', 'E-posta*',
        'Okul Adı*', 'Bölüm', 'Eğitim Düzeyi*', 
        'Sınıf*', 'Rol*'
    ]
    
    # Boş DataFrame oluştur
    df = pd.DataFrame(columns=columns)
    
    # Örnek satır ekle
    df.loc[0] = [
        'ornek.ogrenci', '12345', 'Ahmet', 'Yılmaz',
        '12345678901', '1234', 'ornek@email.com',
        'Örnek Okul', 'Sayısal', 'LISE',
        '10-A', 'STUDENT'
    ]
    
    # Excel dosyası oluştur
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    
    response = HttpResponse(excel_file.read())
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename=ogrenci_sablonu.xlsx'
    
    return response

@login_required
def upload_excel(request):
    """Excel dosyasından öğrenci aktar"""
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        try:
            # Excel dosyasını oku
            df = pd.read_excel(excel_file)
            
            # Zorunlu alanları kontrol et
            required_fields = [
                'Kullanıcı Adı*', 'Şifre*', 'Ad*', 'Soyad*', 
                'TC Kimlik No*', 'Okul No*', 'E-posta*',
                'Okul Adı*', 'Eğitim Düzeyi*', 'Sınıf*', 'Rol*'
            ]
            
            missing_fields = [field for field in required_fields if field not in df.columns]
            if missing_fields:
                messages.error(request, f'Eksik alanlar: {", ".join(missing_fields)}')
                return JsonResponse({
                    'status': 'error',
                    'message': f'Eksik alanlar: {", ".join(missing_fields)}'
                })
            
            success_count = 0
            errors = []
            
            for _, row in df.iterrows():
                try:
                    # Kullanıcı oluştur
                    user = User.objects.create_user(
                        username=row['Kullanıcı Adı*'],
                        password=row['Şifre*'],
                        first_name=row['Ad*'],
                        last_name=row['Soyad*'],
                        email=row['E-posta*']
                    )
                    
                    # Öğrenci oluştur
                    Student.objects.create(
                        user=user,
                        role=row['Rol*'],
                        first_name=row['Ad*'],
                        last_name=row['Soyad*'],
                        tc_no=str(row['TC Kimlik No*']),
                        student_no=str(row['Okul No*']),
                        email=row['E-posta*'],
                        school_name=row['Okul Adı*'],
                        department=row['Bölüm'] if 'Bölüm' in row else '',
                        education_level=row['Eğitim Düzeyi*'],
                        grade=row['Sınıf*'],
                        teacher=request.user.teacher_profile if hasattr(request.user, 'teacher_profile') else None
                    )
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Satır {_ + 2}: {str(e)}")
            
            if success_count > 0:
                messages.success(request, f'{success_count} öğrenci başarıyla eklendi.')
            if errors:
                messages.warning(request, f'{len(errors)} öğrenci eklenirken hata oluştu.')
            
            return JsonResponse({
                'status': 'success',
                'message': f'{success_count} öğrenci başarıyla eklendi.',
                'errors': errors
            })
            
        except Exception as e:
            messages.error(request, f'Dosya işlenirken hata oluştu: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': f'Dosya işlenirken hata oluştu: {str(e)}'
            })
    
    return render(request, 'students/export_excel.html')
