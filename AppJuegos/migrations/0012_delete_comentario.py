# Generated by Django 4.0.4 on 2022-05-22 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppJuegos', '0011_imagen_delete_comentario'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comentario',
        ),
    ]
