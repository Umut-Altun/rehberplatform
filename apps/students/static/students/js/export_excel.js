document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const uploadArea = document.getElementById('uploadArea');
    const excelFile = document.getElementById('excelFile');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const removeFile = document.getElementById('removeFile');
    const uploadButton = document.getElementById('uploadButton');
    const resultArea = document.getElementById('resultArea');
    const resultContent = document.getElementById('resultContent');

    // Dosya sürükle-bırak olayları
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        uploadArea.classList.add('highlight');
    }

    function unhighlight() {
        uploadArea.classList.remove('highlight');
    }

    // Dosya bırakma
    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length) {
            handleFiles(files);
        }
    }

    // Dosya seçimi
    excelFile.addEventListener('change', function() {
        if (this.files.length) {
            handleFiles(this.files);
        }
    });

    function handleFiles(files) {
        const file = files[0];
        
        // Excel dosyası kontrolü
        const validTypes = [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel'
        ];
        
        if (!validTypes.includes(file.type)) {
            alert('Lütfen geçerli bir Excel dosyası seçin (.xlsx veya .xls)');
            return;
        }

        // Dosya bilgisini göster
        fileName.textContent = file.name;
        fileInfo.style.display = 'flex';
        uploadButton.disabled = false;
    }

    // Dosyayı kaldır
    removeFile.addEventListener('click', function() {
        excelFile.value = '';
        fileInfo.style.display = 'none';
        uploadButton.disabled = true;
    });

    // Form gönderimi
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        uploadButton.disabled = true;
        uploadButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Yükleniyor...';
        
        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            // Sonuç alanını göster
            resultArea.style.display = 'block';
            
            if (result.status === 'success') {
                resultContent.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i>
                        <div>
                            <h4>İşlem Başarılı</h4>
                            <p>${result.message}</p>
                            ${result.errors.length ? `
                                <div class="errors-list">
                                    <h5>Hatalar:</h5>
                                    <ul>
                                        ${result.errors.map(error => `<li>${error}</li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                `;
            } else {
                resultContent.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle"></i>
                        <div>
                            <h4>Hata Oluştu</h4>
                            <p>${result.message}</p>
                        </div>
                    </div>
                `;
            }
            
        } catch (error) {
            resultContent.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i>
                    <div>
                        <h4>Hata Oluştu</h4>
                        <p>İşlem sırasında bir hata oluştu. Lütfen tekrar deneyin.</p>
                    </div>
                </div>
            `;
        } finally {
            uploadButton.disabled = false;
            uploadButton.innerHTML = '<i class="fas fa-upload"></i> Yükle ve Aktarmayı Başlat';
        }
    });
});
