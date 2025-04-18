from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from apps.authentication.models import EmailVerification
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@login_required
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Lütfen tüm alanları doldurun!')
            return render(request, 'auth/login.html')
        
        # Önce e-posta ile kontrol et
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            # E-posta bulunamadıysa kullanıcı adıyla devam et
            pass
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'index')
            messages.success(request, f'Hoş geldiniz, {user.get_full_name() or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'E-posta/Kullanıcı adı veya şifre hatalı!')
            return render(request, 'auth/login.html')
            
    return render(request, 'auth/login.html')

def send_verification_email(user, verification_code):
    subject = 'EduPlatform E-posta Doğrulama'
    message = f'Merhaba {user.first_name},\n\nHesabınızı doğrulamak için kodunuz: {verification_code}\n\nSaygılarımızla,\nEduPlatform Ekibi'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            terms = request.POST.get('terms')
            
            # Form validasyonları
            if not all([username, email, password1, password2, first_name, last_name, terms]):
                messages.error(request, 'Lütfen tüm alanları doldurun ve sözleşmeyi kabul edin!')
                return render(request, 'auth/register.html')
            
            # Kullanıcı adı kontrolü
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor!')
                return render(request, 'auth/register.html')
            
            # Email kontrolü    
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Bu e-posta adresi zaten kayıtlı!')
                return render(request, 'auth/register.html')
            
            # Şifre kontrolü
            if password1 != password2:
                messages.error(request, 'Şifreler eşleşmiyor!')
                return render(request, 'auth/register.html')
            
            if len(password1) < 8:
                messages.error(request, 'Şifre en az 8 karakter olmalıdır!')
                return render(request, 'auth/register.html')

            # Kullanıcı oluşturma
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = False
            user.save()
            
            # Email doğrulama kodu oluşturma
            verification = EmailVerification.objects.create(user=user)
            verification_code = verification.generate_verification_code()
            
            # Email gönderme
            try:
                send_verification_email(user, verification_code)
                request.session['verification_email'] = email
                messages.success(request, 'Hesabınız oluşturuldu! Lütfen e-postanıza gönderilen doğrulama kodunu girin.')
                return redirect('verify_email')
            except Exception as e:
                logger.error(f"Email gönderme hatası: {str(e)}")
                user.delete()  # Kullanıcıyı sil
                messages.error(request, 'E-posta gönderilirken bir hata oluştu. Lütfen tekrar deneyin.')
                return render(request, 'auth/register.html')
                
        except Exception as e:
            logger.error(f"Kayıt hatası: {str(e)}")
            messages.error(request, 'Hesap oluşturulurken bir hata oluştu! Lütfen tekrar deneyin.')
            return render(request, 'auth/register.html')
            
    return render(request, 'auth/register.html')

def verify_email_view(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        try:
            verification = EmailVerification.objects.get(
                verification_code=code,
                is_verified=False
            )
            
            if verification:
                user = verification.user
                user.is_active = True
                user.save()
                
                verification.is_verified = True
                verification.save()
                
                messages.success(request, 'E-posta adresiniz başarıyla doğrulandı! Şimdi giriş yapabilirsiniz.')
                return redirect('login')
                
        except EmailVerification.DoesNotExist:
            messages.error(request, 'Geçersiz doğrulama kodu!')
            
    return render(request, 'auth/verify_email.html')

def resend_verification_view(request):
    try:
        # Session'dan email bilgisini al
        email = request.session.get('verification_email')
        if not email:
            messages.error(request, 'Oturum bilgisi bulunamadı. Lütfen tekrar kayıt olun.')
            return redirect('register')

        user = User.objects.get(email=email, is_active=False)
        verification = EmailVerification.objects.get(user=user, is_verified=False)
        
        # Yeni doğrulama kodu oluştur
        verification_code = verification.generate_verification_code()
        
        # E-postayı yeniden gönder
        send_verification_email(user, verification_code)
        
        messages.success(request, 'Doğrulama kodu tekrar gönderildi! Lütfen e-postanızı kontrol edin.')
        return redirect('verify_email')
        
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, 'Geçersiz istek! Lütfen tekrar kayıt olun.')
        return redirect('register')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Mevcut doğrulama kaydını kontrol et
            verification, created = EmailVerification.objects.get_or_create(
                user=user,
                defaults={'is_verified': False}
            )
            
            # Yeni kod oluştur
            verification_code = verification.generate_verification_code()
            verification.is_verified = False
            verification.save()
            
            # E-posta gönder
            subject = 'EduPlatform Şifre Sıfırlama'
            message = f'Merhaba {user.first_name},\n\nŞifre sıfırlama kodunuz: {verification_code}\n\nSaygılarımızla,\nEduPlatform Ekibi'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            
            request.session['reset_email'] = email
            messages.success(request, 'Şifre sıfırlama kodu e-posta adresinize gönderildi!')
            return redirect('reset_password')
            
        except User.DoesNotExist:
            messages.error(request, 'Bu e-posta adresi ile kayıtlı bir hesap bulunamadı!')
            
    return render(request, 'auth/forgot_password.html')

def reset_password_view(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        new_password = request.POST.get('new_password1')
        email = request.session.get('reset_email')
        
        try:
            user = User.objects.get(email=email)
            verification = EmailVerification.objects.get(
                user=user,
                verification_code=code,
                is_verified=False
            )
            
            user.set_password(new_password)
            user.save()
            
            verification.is_verified = True
            verification.save()
            
            messages.success(request, 'Şifreniz başarıyla güncellendi! Şimdi giriş yapabilirsiniz.')
            return redirect('login')
            
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            messages.error(request, 'Geçersiz doğrulama kodu!')
            
    return render(request, 'auth/reset_password.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Başarıyla çıkış yaptınız!')
    return redirect('login')
