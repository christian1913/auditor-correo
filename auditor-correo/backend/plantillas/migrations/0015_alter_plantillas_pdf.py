# Generated by Django 4.1.6 on 2023-06-11 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0014_alter_plantillas_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillas',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='imagenes'),
        ),
    ]