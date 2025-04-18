# Generated by Django 4.2.20 on 2025-04-14 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_add_user_and_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='role',
            field=models.CharField(choices=[('TEACHER', 'Öğretmen'), ('GUEST', 'Misafir'), ('MANAGER', 'Yönetici')], default='TEACHER', max_length=10, verbose_name='Rol'),
        ),
    ]
