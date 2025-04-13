from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    """
    Kullanıcı ayarlarının tutulduğu model
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_settings',
        verbose_name='Kullanıcı'
    )
    theme = models.CharField(
        max_length=20,
        default='light',
        choices=[
            ('light', 'Açık Tema'),
            ('dark', 'Koyu Tema'),
            ('system', 'Sistem Teması')
        ],
        verbose_name='Tema'
    )
    notifications_enabled = models.BooleanField(
        default=True,
        verbose_name='Bildirimler Aktif'
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name='E-posta Bildirimleri'
    )
    language = models.CharField(
        max_length=10,
        default='tr',
        choices=[
            ('tr', 'Türkçe'),
            ('en', 'İngilizce')
        ],
        verbose_name='Dil'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Kullanıcı Ayarı'
        verbose_name_plural = 'Kullanıcı Ayarları'

    def __str__(self):
        return f"{self.user.username} Ayarları"
