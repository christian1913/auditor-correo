# Generated by Django 4.1.6 on 2023-05-29 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registradores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiModelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='imagenes')),
            ],
        ),
    ]
