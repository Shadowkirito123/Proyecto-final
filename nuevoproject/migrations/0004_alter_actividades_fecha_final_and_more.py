# Generated by Django 5.0.6 on 2024-07-09 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevoproject', '0003_alter_actividades_fecha_final_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividades',
            name='fecha_final',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actividades',
            name='fecha_inicio',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
