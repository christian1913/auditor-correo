# Generated by Django 4.1.6 on 2023-06-11 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0011_plantillas_redireccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plantillas',
            name='script',
        ),
        migrations.AlterField(
            model_name='plantillas',
            name='redireccion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='plantillas',
            name='tipo',
            field=models.CharField(choices=[('phishing', 'phishing'), ('acceso', 'acceso')], max_length=20),
        ),
    ]
