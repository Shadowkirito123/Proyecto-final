# Generated by Django 5.0.6 on 2024-07-11 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevoproject', '0004_alter_actividades_fecha_final_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profesores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('apellido', models.CharField(max_length=250)),
                ('materia', models.CharField(max_length=250)),
                ('estado', models.BooleanField(default=False)),
            ],
        ),
    ]
