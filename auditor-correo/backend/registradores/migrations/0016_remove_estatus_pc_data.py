# Generated by Django 4.1.6 on 2023-06-13 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registradores', '0015_remove_credenciales_enviado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estatus_pc',
            name='data',
        ),
    ]