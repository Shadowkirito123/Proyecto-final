# Generated by Django 5.0.6 on 2024-09-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuevoproject', '0033_alter_actividades_metas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividades',
            name='metas',
            field=models.TextField(),
        ),
    ]
