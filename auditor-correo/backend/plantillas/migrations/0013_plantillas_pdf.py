# Generated by Django 4.1.6 on 2023-06-11 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0012_remove_plantillas_script_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantillas',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs'),
        ),
    ]
