from django.db import models
from django.db.models import PROTECT
from django.contrib.auth.models import User

class Student(models.Model):
    EDUCATION_LEVELS = [
        ('ILK', 'İlkokul'),
        ('ORTA', 'Ortaokul'),
        ('LISE', 'Lise'),
        ('UNI', 'Üniversite')
    ]
    
    ROLE_CHOICES = [
        ('STUDENT', 'Öğrenci'),
        ('GUEST', 'Misafir')
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Kullanıcı'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT',
        verbose_name='Rol'
    )
    first_name = models.CharField(max_length=50, verbose_name='Ad')
    last_name = models.CharField(max_length=50, verbose_name='Soyad')
    tc_no = models.CharField(max_length=11, unique=True, verbose_name='TC Kimlik No')
    student_no = models.CharField(max_length=20, verbose_name='Okul No')
    email = models.EmailField(verbose_name='E-posta')
    school_name = models.CharField(max_length=100, verbose_name='Okul Adı')
    department = models.CharField(max_length=100, verbose_name='Bölüm', blank=True)
    education_level = models.CharField(
        max_length=4,
        choices=EDUCATION_LEVELS,
        verbose_name='Eğitim Düzeyi'
    )
    grade = models.CharField(max_length=20, verbose_name='Sınıf')
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=PROTECT,
        null=True,
        blank=True,
        verbose_name='Öğretmen',
        related_name='students'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Öğrenci'
        verbose_name_plural = 'Öğrenciler'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.tc_no}"

    def save(self, *args, **kwargs):
        # Kullanıcı bilgilerini senkronize et
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs)
