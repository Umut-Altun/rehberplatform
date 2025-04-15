from django.contrib import admin
from .models import ErrorReport
from django.utils.translation import gettext_lazy as _

@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    """Admin view for ErrorReport model."""
    list_display = ('report_type', 'user_display', 'created_at', 'resolved', 'page_url_short')
    list_filter = ('report_type', 'resolved', 'created_at')
    search_fields = ('description', 'user__username', 'user__email', 'page_url')
    list_editable = ('resolved',)
    readonly_fields = ('user', 'created_at', 'page_url')
    fieldsets = (
        (_("Bildirim Detayları"), {
            'fields': ('report_type', 'description', 'page_url')
        }),
        (_("Durum ve Kullanıcı Bilgisi"), {
            'fields': ('resolved', 'user', 'created_at')
        }),
    )

    def user_display(self, obj):
        return obj.user.username if obj.user else _("Anonim")
    user_display.short_description = _("Bildiren Kullanıcı")

    def page_url_short(self, obj):
        if obj.page_url and len(obj.page_url) > 50:
            return f"{obj.page_url[:50]}..."
        return obj.page_url
    page_url_short.short_description = _("Sayfa URL") 