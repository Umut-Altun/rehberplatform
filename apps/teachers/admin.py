from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'tc_no', 'branch', 'school_name', 'experience_years')
    search_fields = ('first_name', 'last_name', 'tc_no', 'email', 'phone')
    list_filter = ('branch', 'school_name')
    ordering = ('-created_at',) 