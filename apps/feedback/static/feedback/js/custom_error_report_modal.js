document.addEventListener('DOMContentLoaded', function() {

    const reportErrorButtonNavbar = document.getElementById('reportErrorBtn');
    const customModalOverlay = document.getElementById('customErrorReportModalOverlay');
    const customModalForm = document.getElementById('customErrorReportForm');
    const closeCustomModalBtn = document.getElementById('closeCustomErrorModalBtn');
    const cancelCustomModalBtn = document.getElementById('cancelCustomErrorModalBtn');
    const submitCustomReportButton = document.getElementById('submitCustomReportButton');
    const customReportErrorFormAlert = document.getElementById('customReportErrorFormAlert');
    const pageUrlInput = customModalForm ? customModalForm.querySelector('input[name="page_url"]') : null;
    const spinner = submitCustomReportButton ? submitCustomReportButton.querySelector('.spinner') : null;

    function openModal() {
        if (!customModalOverlay) return;
        // Formu ve alert'i sıfırla
        if(customModalForm) customModalForm.reset();
        if(customReportErrorFormAlert) {
             customReportErrorFormAlert.style.display = 'none';
             customReportErrorFormAlert.textContent = '';
             customReportErrorFormAlert.className = 'custom-alert'; // Reset classes
        }
        if(submitCustomReportButton) submitCustomReportButton.disabled = false;
        if(spinner) spinner.style.display = 'none';
        // Mevcut sayfa URL'sini gizli alana ekle
        if(pageUrlInput) pageUrlInput.value = window.location.href;
        // Modalı göster
        customModalOverlay.style.display = 'flex';
        setTimeout(() => { // Kısa bir gecikmeyle aktif sınıfını ekle (animasyon için)
            customModalOverlay.classList.add('active');
        }, 10); 
    }

    function closeModal() {
        if (!customModalOverlay) return;
        customModalOverlay.classList.remove('active');
        // Animasyon bittikten sonra gizle
        setTimeout(() => {
            customModalOverlay.style.display = 'none';
        }, 300); // CSS transition süresiyle eşleşmeli
    }

    // Navbar'daki butona tıklanınca modalı aç
    if (reportErrorButtonNavbar) {
        reportErrorButtonNavbar.addEventListener('click', function(event) {
            event.preventDefault();
            openModal();
        });
    }

    // Kapatma (X) butonuna tıklanınca modalı kapat
    if (closeCustomModalBtn) {
        closeCustomModalBtn.addEventListener('click', closeModal);
    }

    // Vazgeç butonuna tıklanınca modalı kapat
    if (cancelCustomModalBtn) {
        cancelCustomModalBtn.addEventListener('click', closeModal);
    }

    // Overlay'e tıklanınca modalı kapat (isteğe bağlı)
    if (customModalOverlay) {
        customModalOverlay.addEventListener('click', function(event) {
            if (event.target === customModalOverlay) { // Sadece overlay'e tıklandıysa
                closeModal();
            }
        });
    }

    // Form gönderimini AJAX ile handle et
    if (customModalForm) {
        customModalForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Formun normal gönderimini engelle

            if(submitCustomReportButton) submitCustomReportButton.disabled = true;
            if(spinner) spinner.style.display = 'inline-block';
            if(customReportErrorFormAlert) customReportErrorFormAlert.style.display = 'none';

            const formData = new FormData(customModalForm);
            const url = customModalForm.action;
            const csrfToken = getCookie('csrftoken');

            if (!csrfToken) {
                displayAlert('Güvenlik anahtarı bulunamadı. Sayfayı yenileyip tekrar deneyin.', 'danger');
                if(submitCustomReportButton) submitCustomReportButton.disabled = false;
                if(spinner) spinner.style.display = 'none';
                return;
            }
            // FormData içinde CSRF token zaten var, header'a gerek yok

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw { status: response.status, data: errorData };
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    displayAlert(data.message || 'Hata bildiriminiz başarıyla alındı!', 'success');
                    setTimeout(closeModal, 2000); // Başarıdan 2sn sonra kapat
                } else {
                    let errorMessage = data.message || 'Bir hata oluştu.';
                    if (data.errors) {
                         // Şimdilik sadece genel mesajda gösterelim
                        errorMessage += "\nDetaylar: " + JSON.stringify(data.errors);
                    }
                    displayAlert(errorMessage, 'danger');
                }
            })
            .catch(error => {
                console.error('Hata Bildirimi Gönderilemedi:', error);
                let message = 'Hata bildirimi gönderilirken bir sorun oluştu.';
                if (error && error.data && error.data.message) {
                    message = error.data.message;
                } else if (error && error.status) {
                    message += ` (Hata Kodu: ${error.status})`;
                }
                 displayAlert(message, 'danger');
            })
            .finally(() => {
                if(submitCustomReportButton) submitCustomReportButton.disabled = false;
                if(spinner) spinner.style.display = 'none';
            });
        });
    }

    // Modal içinde uyarı gösterme fonksiyonu
    function displayAlert(message, type = 'danger') { // type: 'success' or 'danger'
        if (!customReportErrorFormAlert) return;
        customReportErrorFormAlert.textContent = message;
        customReportErrorFormAlert.className = 'custom-alert'; // Reset classes
        customReportErrorFormAlert.classList.add(`alert-${type}`);
        customReportErrorFormAlert.style.display = 'block';
    }

    // CSRF token'ı cookie'den almak için yardımcı fonksiyon (önceden vardı)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

}); 