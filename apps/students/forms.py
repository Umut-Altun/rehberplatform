from django import forms
from django.core.validators import RegexValidator
from .models import Student

class StudentForm(forms.ModelForm):
    tc_validator = RegexValidator(
        regex=r'^\d{11}$',
        message='TC Kimlik No 11 haneli olmalıdır.'
    )
    
    student_no_validator = RegexValidator(
        regex=r'^\d+$',
        message='Öğrenci numarası sadece rakamlardan oluşmalıdır.'
    )

    tc_no = forms.CharField(
        validators=[tc_validator],
        max_length=11,
        min_length=11
    )
    
    student_no = forms.CharField(
        validators=[student_no_validator],
        max_length=20
    )

    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'tc_no', 'student_no',
            'email', 'school_name', 'department', 'education_level',
            'grade', 'role', 'teacher'
        ]
        labels = {
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'tc_no': 'TC Kimlik No',
            'student_no': 'Öğrenci No',
            'email': 'E-posta',
            'school_name': 'Okul Adı',
            'department': 'Bölüm',
            'education_level': 'Eğitim Seviyesi',
            'grade': 'Sınıf',
            'role': 'Rol',
            'teacher': 'Öğretmen'
        }

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)
        
        if not edit_mode:
            # Yeni öğrenci ekleme alanları
            self.fields['username'] = forms.CharField(
                max_length=150,
                label='Kullanıcı Adı',
                help_text='Giriş yaparken kullanılacak benzersiz kullanıcı adı'
            )
            self.fields['password'] = forms.CharField(
                widget=forms.PasswordInput,
                label='Şifre',
                min_length=6
            )
            self.fields['password_confirm'] = forms.CharField(
                widget=forms.PasswordInput,
                label='Şifre (Tekrar)',
                min_length=6
            )

        # Tüm alanlar için gereklilik kontrolü
        for field in self.fields:
            self.fields[field].required = True
            if field != 'department':  # Bölüm alanı opsiyonel olabilir
                self.fields[field].widget.attrs['required'] = 'required'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Şifreler eşleşmiyor!')

        return cleaned_data

    def clean_tc_no(self):
        tc_no = self.cleaned_data.get('tc_no')
        if tc_no:
            # TC No benzersizlik kontrolü
            exists = Student.objects.filter(tc_no=tc_no)
            if self.instance:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise forms.ValidationError('Bu TC Kimlik No ile kayıtlı başka bir öğrenci var!')
        return tc_no

    def clean_student_no(self):
        student_no = self.cleaned_data.get('student_no')
        if student_no:
            # Öğrenci No benzersizlik kontrolü
            exists = Student.objects.filter(student_no=student_no)
            if self.instance:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise forms.ValidationError('Bu Öğrenci No ile kayıtlı başka bir öğrenci var!')
        return student_no
