from django.contrib import admin
from .models import UserSettings

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'notifications_enabled', 'email_notifications', 'language', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('theme', 'notifications_enabled', 'email_notifications', 'language')

admin.site.register(UserSettings, UserSettingsAdmin)
