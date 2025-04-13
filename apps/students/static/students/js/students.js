// Öğrenciler sayfası için JavaScript fonksiyonları buraya gelecek 

// CSRF token'ı almak için yardımcı fonksiyon
function getCsrfToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}

// Modal HTML'ini oluştur
function createDeleteModal() {
    const modalHTML = `
        <div class="modal-overlay" id="deleteModal">
            <div class="modal">
                <div class="modal-header">
                    <i class="fas fa-exclamation-triangle modal-icon"></i>
                    <h2 class="modal-title">Öğrenciyi Silmek İstediğinize Emin misiniz?</h2>
                </div>
                <div class="modal-body">
                    <p class="modal-message">Bu öğrenciyi silmek üzeresiniz. Bu işlem geri alınamaz.</p>
                </div>
                <div class="modal-actions">
                    <button class="modal-btn modal-btn-cancel" id="cancelDelete">
                        <i class="fas fa-times"></i>
                        İptal
                    </button>
                    <button class="modal-btn modal-btn-delete" id="confirmDelete">
                        <i class="fas fa-trash"></i>
                        Sil
                    </button>
                </div>
            </div>
        </div>
    `;

    // Modal'ı body'ye ekle
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Modal elementlerini seç
    const modal = document.getElementById('deleteModal');
    const cancelBtn = document.getElementById('cancelDelete');
    const confirmBtn = document.getElementById('confirmDelete');

    // Modal'ı kapat
    function closeModal() {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }

    // İptal butonuna tıklanınca
    cancelBtn.addEventListener('click', closeModal);

    // Modal dışına tıklanınca
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // ESC tuşuna basılınca
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
        }
    });

    return {
        modal,
        confirmBtn,
        close: closeModal
    };
}

// Silme işlemi için event listener
document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', async (e) => {
        const deleteBtn = e.target.closest('.btn-danger');
        if (deleteBtn) {
            e.preventDefault();
            const studentId = deleteBtn.dataset.studentId;
            const studentName = deleteBtn.dataset.studentName;

            // Modal'ı oluştur ve göster
            const { modal, confirmBtn, close } = createDeleteModal();
            
            // Öğrenci adını mesaja ekle
            const messageEl = modal.querySelector('.modal-message');
            messageEl.textContent = `${studentName} isimli öğrenciyi silmek üzeresiniz. Bu işlem geri alınamaz.`;

            // Modal'ı göster
            setTimeout(() => {
                modal.classList.add('active');
            }, 10);

            // Silme onayı
            confirmBtn.addEventListener('click', async () => {
                try {
                    const response = await fetch(`/students/${studentId}/delete/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCsrfToken(),
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    if (response.ok) {
                        // Başarılı silme işlemi
                        const studentCard = deleteBtn.closest('.student-card');
                        studentCard.style.transition = 'all 0.3s ease';
                        studentCard.style.transform = 'scale(0.9)';
                        studentCard.style.opacity = '0';
                        
                        setTimeout(() => {
                            studentCard.remove();
                            // Eğer hiç öğrenci kalmadıysa
                            const remainingCards = document.querySelectorAll('.student-card');
                            if (remainingCards.length === 0) {
                                location.reload(); // Sayfayı yenile
                            }
                        }, 300);
                        
                        close();
                    } else {
                        throw new Error('Silme işlemi başarısız oldu');
                    }
                } catch (error) {
                    console.error('Hata:', error);
                    messageEl.textContent = 'Bir hata oluştu. Lütfen tekrar deneyin.';
                    messageEl.style.color = '#e74c3c';
                }
            });
        }
    });
});

// Arama tipi seçimi
document.addEventListener('DOMContentLoaded', function() {
    const searchTypeTexts = document.querySelectorAll('.search-type-text');
    const searchTypeInput = document.getElementById('search-type');
    const searchInput = document.querySelector('.search-input');

    // URL'den mevcut arama tipini al
    const urlParams = new URLSearchParams(window.location.search);
    const currentType = urlParams.get('type') || 'name';

    // Başlangıçta doğru tipi seç
    searchTypeInput.value = currentType;
    searchTypeTexts.forEach(text => {
        if (text.dataset.type === currentType) {
            text.classList.add('active');
        }
    });

    // Arama tipi tıklama olayları
    searchTypeTexts.forEach(text => {
        text.addEventListener('click', function() {
            // Aktif sınıfını kaldır
            searchTypeTexts.forEach(t => t.classList.remove('active'));
            
            // Seçilen tipe aktif sınıfını ekle
            this.classList.add('active');
            
            // Hidden input değerini güncelle
            searchTypeInput.value = this.dataset.type;
            
            // Placeholder metnini güncelle
            if (this.dataset.type === 'tc') {
                searchInput.placeholder = 'TC Kimlik No ile ara...';
            } else {
                searchInput.placeholder = 'İsim ile ara...';
            }
        });
    });
}); 