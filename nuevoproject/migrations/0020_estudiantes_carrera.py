# Generated by Django 5.0.6 on 2024-07-25 00:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevoproject', '0019_estdiantes_por_carreras_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiantes',
            name='carrera',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nuevoproject.carreras'),
        ),
    ]
