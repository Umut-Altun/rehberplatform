document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('message-container');
    if (!messageContainer) return;

    function removeMessage(messageBox) {
        return new Promise((resolve) => {
            messageBox.classList.add('removing');
            
            messageBox.addEventListener('animationend', () => {
                messageBox.remove();
                
                // Container'ı kontrol et ve güncelle
                if (messageContainer.children.length === 0) {
                    messageContainer.style.display = 'none';
                }
                resolve();
            }, { once: true }); // Event listener'ı bir kez çalıştır ve temizle
        });
    }

    async function initializeMessage(messageBox) {
        // Kapatma butonunu bul veya oluştur
        let closeBtn = messageBox.querySelector('.message-close');
        if (!closeBtn) {
            closeBtn = document.createElement('button');
            closeBtn.className = 'message-close';
            closeBtn.setAttribute('aria-label', 'Kapat');
            closeBtn.innerHTML = '<i class="fas fa-times"></i>';
            messageBox.appendChild(closeBtn);
        }

        // Kapatma butonu olayı
        closeBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            await removeMessage(messageBox);
        }, { once: true });

        // Otomatik kapatma için zamanlayıcı
        if (messageBox.classList.contains('success') || 
            messageBox.classList.contains('info')) {
            setTimeout(async () => {
                if (messageBox && messageBox.isConnected) {
                    await removeMessage(messageBox);
                }
            }, 5000); // 5 saniye sonra otomatik kapat
        }
    }

    // Mevcut mesajları başlat
    document.querySelectorAll('.message-box').forEach(initializeMessage);

    // Global mesaj gösterme fonksiyonu
    window.showMessage = function(message, type = 'info') {
        const messageBox = document.createElement('div');
        messageBox.className = `message-box ${type}`;
        
        const title = {
            'success': 'Başarılı!',
            'error': 'Hata!',
            'warning': 'Uyarı!',
            'info': 'Bilgi'
        }[type] || 'Bilgi';

        const icon = {
            'success': 'fa-check-circle',
            'error': 'fa-times-circle',
            'warning': 'fa-exclamation-circle',
            'info': 'fa-info-circle'
        }[type] || 'fa-info-circle';

        messageBox.innerHTML = `
            <div class="message-content">
                <i class="message-icon fas ${icon}"></i>
                <div class="message-text">
                    <h4>${title}</h4>
                    <p>${message}</p>
                </div>
            </div>
        `;

        messageContainer.style.display = 'flex';
        messageContainer.appendChild(messageBox);
        initializeMessage(messageBox);
    };
});
