from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.contrib.auth.hashers import make_password

def create_users_for_existing_teachers(apps, schema_editor):
    Teacher = apps.get_model('teachers', 'Teacher')
    User = apps.get_model('auth', 'User')
    
    for teacher in Teacher.objects.all():
        # TC no'yu kullanıcı adı olarak kullan
        username = f"teacher_{teacher.tc_no}"
        # Varsayılan şifre olarak TC no kullan
        password = make_password(teacher.tc_no)
        
        user = User.objects.create(
            username=username,
            password=password,
            email=teacher.email,
            first_name=teacher.first_name,
            last_name=teacher.last_name
        )
        
        teacher.user = user
        teacher.role = 'TEACHER'  # Varsayılan rol
        teacher.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='role',
            field=models.CharField(
                choices=[
                    ('STUDENT', 'Öğrenci'),
                    ('TEACHER', 'Öğretmen'),
                    ('ADMIN', 'Admin'),
                    ('GUEST', 'Misafir'),
                    ('MANAGER', 'Yönetici')
                ],
                default='TEACHER',
                max_length=10,
                verbose_name='Rol'
            ),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='teacher_profile',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Kullanıcı'
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            create_users_for_existing_teachers,
            reverse_code=migrations.RunPython.noop
        ),
    ] 