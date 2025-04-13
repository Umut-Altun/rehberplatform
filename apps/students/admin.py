from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'tc_no', 'education_level', 'grade', 'school_name')
    search_fields = ('first_name', 'last_name', 'tc_no', 'student_no', 'email')
    list_filter = ('education_level', 'grade')
    ordering = ('-created_at',)
