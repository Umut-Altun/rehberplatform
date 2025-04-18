from django.contrib import admin
from .models import EmailVerification

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_code', 'created_at', 'is_verified')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'verification_code')
    readonly_fields = ('created_at',)
