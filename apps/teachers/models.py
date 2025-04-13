from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    BRANCH_CHOICES = [
        ('MAT', 'Matematik'),
        ('FEN', 'Fen Bilimleri'),
        ('TUR', 'Türkçe'),
        ('SOS', 'Sosyal Bilgiler'),
        ('ING', 'İngilizce'),
        ('BIL', 'Bilişim'),
        ('DIG', 'Diğer')
    ]
    
    ROLE_CHOICES = [
        ('TEACHER', 'Öğretmen'),
        ('GUEST', 'Misafir'),
        ('MANAGER', 'Yönetici')
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name='Kullanıcı'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='TEACHER',
        verbose_name='Rol'
    )
    first_name = models.CharField(max_length=50, verbose_name='Ad')
    last_name = models.CharField(max_length=50, verbose_name='Soyad')
    tc_no = models.CharField(max_length=11, unique=True, verbose_name='TC Kimlik No')
    email = models.EmailField(verbose_name='E-posta')
    phone = models.CharField(max_length=15, verbose_name='Telefon')
    branch = models.CharField(max_length=3, choices=BRANCH_CHOICES, verbose_name='Branş')
    school_name = models.CharField(max_length=100, verbose_name='Okul Adı')
    experience_years = models.PositiveIntegerField(verbose_name='Deneyim (Yıl)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Öğretmen'
        verbose_name_plural = 'Öğretmenler'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_branch_display()}"
        
    def save(self, *args, **kwargs):
        # Kullanıcı bilgilerini senkronize et
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs) 