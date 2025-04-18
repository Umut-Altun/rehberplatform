from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

# Kullanıcı kayıt formu, kullanıcıdan gerekli bilgileri alır ve yeni bir kullanıcı oluşturur.
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Kullanıcı giriş formu, kullanıcıdan e-posta veya kullanıcı adı ve sifre alır ve kullanıcıyı doğrular.
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='E-posta veya Kullanıcı Adı')
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            # E-posta ile giriş denemesi
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    raise ValidationError(
                        "Bu e-posta adresi ile kayıtlı bir hesap bulunamadı.",
                        code='invalid_login',
                    )

            self.user_cache = authenticate(
                self.request, username=username, password=password)
            
            if self.user_cache is None:
                raise ValidationError(
                    "Lütfen doğru kullanıcı adı/e-posta ve şifre giriniz.",
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data 
    


