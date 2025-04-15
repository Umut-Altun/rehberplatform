document.addEventListener('DOMContentLoaded', function() {
    // Bildirim kapatma işlevi
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        });
    });

    // Otomatik bildirim kapatma
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        });
    }, 5000);

    // AJAX form gönderimi
    const forms = document.querySelectorAll('#profile-form, #password-form, #settings-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const url = this.getAttribute('action');
            const formId = this.getAttribute('id');
            
            // Form gönderimi sırasında butonun görünümünü değiştir
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> İşleniyor...';
            submitButton.disabled = true;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Butonun görünümünü eski haline getir
                submitButton.innerHTML = originalButtonText;
                submitButton.disabled = false;
                
                if (data.status === 'success') {
                    // Şifre değiştirme formunu temizle
                    if (formId === 'password-form') {
                        form.reset();
                    }
                    // Başarılı işlem sonrası sayfayı yenile
                    window.location.reload();
                } else if (data.status === 'error') {
                    // Hata mesajlarını göster
                    for (const field in data.errors) {
                        // İlgili alana hata sınıfı ekle
                        const inputField = document.querySelector(`#id_${field}`);
                        if (inputField) {
                            inputField.classList.add('error-field');
                            
                            // Hata mesajını göster
                            let errorElement = inputField.parentNode.querySelector('.field-error');
                            if (!errorElement) {
                                errorElement = document.createElement('div');
                                errorElement.className = 'field-error';
                                inputField.parentNode.appendChild(errorElement);
                            }
                            errorElement.textContent = data.errors[field].join(', ');
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitButton.innerHTML = originalButtonText;
                submitButton.disabled = false;
            });
        });
    });
    
    // Form alanlarındaki hata gösterimini temizle
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(input => {
        input.addEventListener('focus', function() {
            this.classList.remove('error-field');
            const errorElement = this.parentNode.querySelector('.field-error');
            if (errorElement) {
                errorElement.remove();
            }
        });
    });
    
    // Bildirim gösterme fonksiyonu
    function showMessage(type, message) {
        // Varsa önceki bildirim konteynerini temizle
        const existingContainer = document.querySelector('.messages-container');
        if (existingContainer) {
            existingContainer.remove();
        }
        
        // Yeni bildirim konteyneri oluştur
        const messagesContainer = document.createElement('div');
        messagesContainer.className = 'messages-container';
        
        // Bildirim oluştur
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            ${message}
            <button type="button" class="close-alert">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Bildirim konteynerine ekle
        messagesContainer.appendChild(alert);
        
        // Sayfaya ekle
        const settingsContainer = document.querySelector('.settings-container');
        settingsContainer.insertBefore(messagesContainer, settingsContainer.querySelector('.settings-tabs'));
        
        // Kapatma düğmesine olay dinleyicisi ekle
        const closeButton = alert.querySelector('.close-alert');
        closeButton.addEventListener('click', function() {
            alert.style.opacity = '0';
            setTimeout(() => {
                messagesContainer.remove();
            }, 300);
        });
        
        // Otomatik kapanma zamanlayıcısı
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                messagesContainer.remove();
            }, 300);
        }, 5000);
    }
}); 