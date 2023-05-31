# Generated by Django 4.1.6 on 2023-05-29 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smtp', '0003_remove_enviados_mail_status_id_and_more'),
        ('registradores', '0002_mimodelo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status_mail',
            name='propietario',
        ),
        migrations.RemoveField(
            model_name='status_pc',
            name='propietario',
        ),
        migrations.RemoveField(
            model_name='status_web',
            name='propietario',
        ),
        migrations.AddField(
            model_name='status_mail',
            name='envido',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='smtp.enviados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_pc',
            name='enviado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='smtp.enviados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_web',
            name='enviado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='smtp.enviados'),
            preserve_default=False,
        ),
    ]
