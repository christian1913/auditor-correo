# Generated by Django 4.1.6 on 2023-05-30 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smtp', '0005_enviados_estatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enviados',
            name='estatus',
        ),
        migrations.DeleteModel(
            name='Credenciales',
        ),
    ]