from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .forms import UserProfileForm, UserSettingsForm, CustomPasswordChangeForm
from .models import UserSettings

@login_required
def settings_home(request):
    """
    Ayarlar sayfası ana görünümü
    """
    # Kullanıcının ayarlarını al veya oluştur
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    # Varsayılan olarak "profile" sekmesini göster
    active_tab = request.GET.get('tab', 'profile')
    
    # Formları hazırla
    profile_form = UserProfileForm(instance=request.user)
    settings_form = UserSettingsForm(instance=user_settings)
    password_form = CustomPasswordChangeForm(user=request.user)
    
    context = {
        'active_page': 'settings',
        'active_tab': active_tab,
        'profile_form': profile_form,
        'settings_form': settings_form,
        'password_form': password_form,
    }
    return render(request, 'settings/settings_home.html', context)

@login_required
def update_profile(request):
    """
    Kullanıcı profil bilgilerini güncelleme
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            
            # AJAX isteği ise
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            
            return redirect('settings:home')
        else:
            # AJAX isteği ise
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'settings/profile_form.html', {'form': form})

@login_required
def update_settings(request):
    """
    Kullanıcı ayarlarını güncelleme
    """
    # Kullanıcının ayarlarını al veya oluştur
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            
            # AJAX isteği ise
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
                
            return redirect('settings:home')
        else:
            # AJAX isteği ise
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = UserSettingsForm(instance=user_settings)
    
    return render(request, 'settings/settings_form.html', {'form': form})

@login_required
def change_password(request):
    """
    Kullanıcı şifre değiştirme
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Session'ı güncelle, kullanıcı çıkışını engelle
            update_session_auth_hash(request, user)
            
            # AJAX isteği ise
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
                
            return redirect('settings:home')
        else:
            # AJAX isteği ise
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'settings/password_form.html', {'form': form})
