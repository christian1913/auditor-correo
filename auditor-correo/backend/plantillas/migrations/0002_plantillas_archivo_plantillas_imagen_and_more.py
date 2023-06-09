# Generated by Django 4.1.6 on 2023-05-29 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantillas',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='plantillas',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='ruta/para/subir/'),
        ),
        migrations.AddField(
            model_name='plantillas',
            name='plantilla',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
