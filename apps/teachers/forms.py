from django import forms
from django.contrib.auth.models import User
from .models import Teacher

class TeacherForm(forms.ModelForm):
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
        model = Teacher
        fields = [
            'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'tc_no', 'email',
            'phone', 'branch', 'school_name', 'experience_years',
            'role'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyad'}),
            'tc_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TC Kimlik No'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Okul Adı'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Deneyim (Yıl)'}),
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

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.replace(' ', '').isdigit():
            raise forms.ValidationError('Telefon numarası sadece rakam içermelidir.')
        return phone
        
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
        teacher = super().save(commit=False)
        
        # Yeni kullanıcı oluştur
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        teacher.user = user
        
        if commit:
            teacher.save()
        
        return teacher 