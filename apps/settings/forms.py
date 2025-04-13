from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserSettings

class UserProfileForm(forms.ModelForm):
    """
    Kullanıcı profil bilgilerini güncellemek için form
    """
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ad'
        }),
        label="Ad"
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Soyad'
        }),
        label="Soyad"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-posta'
        }),
        label="E-posta"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Şifre değiştirme formu
    """
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mevcut Şifre'
        }),
        label="Mevcut Şifre"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni Şifre'
        }),
        label="Yeni Şifre"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni Şifre (Tekrar)'
        }),
        label="Yeni Şifre (Tekrar)"
    )

class UserSettingsForm(forms.ModelForm):
    """
    Kullanıcı ayarlarını güncellemek için form
    """
    class Meta:
        model = UserSettings
        fields = ['theme', 'notifications_enabled', 'email_notifications', 'language']
        widgets = {
            'theme': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notifications_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'language': forms.Select(attrs={
                'class': 'form-control'
            })
        }
