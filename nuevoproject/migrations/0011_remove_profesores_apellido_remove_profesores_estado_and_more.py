# Generated by Django 5.0.6 on 2024-07-13 21:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevoproject', '0010_remove_materia_actividad_actividades_materia'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profesores',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='profesores',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='profesores',
            name='materia',
        ),
        migrations.RemoveField(
            model_name='profesores',
            name='nombre',
        ),
        migrations.AddField(
            model_name='profesores',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Estudiantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
