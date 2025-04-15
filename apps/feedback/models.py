from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ErrorReport(models.Model):
    """Model to store user error reports."""
    
    class ReportType(models.TextChoices):
        BUG = 'BUG', _('Yazılım Hatası')
        UI_UX = 'UI_UX', _('Arayüz/Kullanıcı Deneyimi Sorunu')
        FUNCTIONALITY = 'FUNCTIONALITY', _('İşlevsellik Sorunu')
        PERFORMANCE = 'PERFORMANCE', _('Performans Sorunu')
        OTHER = 'OTHER', _('Diğer')

    report_type = models.CharField(
        _("Hata Türü"),
        max_length=20,
        choices=ReportType.choices,
        default=ReportType.OTHER,
    )
    description = models.TextField(
        _("Açıklama"),
        help_text=_("Lütfen karşılaştığınız hatayı detaylı bir şekilde açıklayın.")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Bildiren Kullanıcı"),
        related_name='error_reports'
    )
    created_at = models.DateTimeField(
        _("Bildirim Zamanı"),
        auto_now_add=True
    )
    resolved = models.BooleanField(
        _("Çözüldü mü?"),
        default=False
    )
    page_url = models.URLField(
        _("Hatanın Olduğu Sayfa URL'si"),
        max_length=1024,
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = _("Hata Bildirimi")
        verbose_name_plural = _("Hata Bildirimleri")
        ordering = ['-created_at']

    def __str__(self):
        user_info = self.user.username if self.user else _("Anonim")
        return f"{self.get_report_type_display()} - {user_info} ({self.created_at.strftime('%d.%m.%Y %H:%M')})" 