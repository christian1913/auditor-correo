# Generated by Django 4.1.6 on 2023-05-31 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0010_remove_plantillas_usuario_opcional'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantillas',
            name='redireccion',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]