# Generated by Django 5.0.6 on 2024-07-25 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevoproject', '0020_estudiantes_carrera'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materias_por_carreras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrera', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='nuevoproject.carreras')),
                ('materia', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='nuevoproject.materia')),
            ],
        ),
    ]
