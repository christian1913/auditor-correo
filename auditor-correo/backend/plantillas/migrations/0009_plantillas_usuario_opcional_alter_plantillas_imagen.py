# Generated by Django 4.1.6 on 2023-05-31 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0008_plantillas_propietario'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantillas',
            name='usuario_opcional',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plantillas',
            name='imagen',
            field=models.ImageField(upload_to='imagenes'),
        ),
    ]