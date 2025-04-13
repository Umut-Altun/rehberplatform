from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.contrib.auth.hashers import make_password

def create_users_for_existing_students(apps, schema_editor):
    Student = apps.get_model('students', 'Student')
    User = apps.get_model('auth', 'User')
    
    for student in Student.objects.all():
        # TC no'yu kullanıcı adı olarak kullan
        username = f"student_{student.tc_no}"
        # Varsayılan şifre olarak TC no kullan
        password = make_password(student.tc_no)
        
        user = User.objects.create(
            username=username,
            password=password,
            email=student.email,
            first_name=student.first_name,
            last_name=student.last_name
        )
        
        student.user = user
        student.role = 'STUDENT'  # Varsayılan rol
        student.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='role',
            field=models.CharField(
                choices=[
                    ('STUDENT', 'Öğrenci'),
                    ('TEACHER', 'Öğretmen'),
                    ('ADMIN', 'Admin'),
                    ('GUEST', 'Misafir'),
                    ('MANAGER', 'Yönetici')
                ],
                default='STUDENT',
                max_length=10,
                verbose_name='Rol'
            ),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='student_profile',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Kullanıcı'
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            create_users_for_existing_students,
            reverse_code=migrations.RunPython.noop
        ),
    ] 