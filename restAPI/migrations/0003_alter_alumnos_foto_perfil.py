# Generated by Django 3.2.13 on 2022-05-26 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0002_alumnos_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnos',
            name='foto_perfil',
            field=models.FileField(upload_to='media/'),
        ),
    ]
