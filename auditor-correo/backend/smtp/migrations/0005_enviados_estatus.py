# Generated by Django 4.1.6 on 2023-05-30 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smtp', '0004_credenciales'),
    ]

    operations = [
        migrations.AddField(
            model_name='enviados',
            name='estatus',
            field=models.BooleanField(default=False),
        ),
    ]