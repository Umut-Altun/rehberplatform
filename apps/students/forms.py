from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı Adı'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre'
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre (Tekrar)'
        })
    )

    class Meta:
        model = Student
        fields = [
            'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'tc_no', 'student_no',
            'email', 'school_name', 'department', 'education_level', 'grade',
            'teacher', 'role'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyad'}),
            'tc_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TC Kimlik No'}),
            'student_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Okul No'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Okul Adı'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bölüm'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sınıf'}),
            'teacher': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Öğretmen Seçin'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Rol Seçin'
            }),
        }

    def clean_tc_no(self):
        tc_no = self.cleaned_data.get('tc_no')
        if not tc_no.isdigit() or len(tc_no) != 11:
            raise forms.ValidationError('TC Kimlik No 11 haneli sayısal bir değer olmalıdır.')
        return tc_no

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        username = cleaned_data.get('username')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Şifreler eşleşmiyor.')

        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Bu kullanıcı adı zaten kullanılıyor.')

        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        
        # Yeni kullanıcı oluştur
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        student.user = user
        
        if commit:
            student.save()
        
        return student
