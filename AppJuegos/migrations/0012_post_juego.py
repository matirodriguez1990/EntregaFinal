# Generated by Django 4.0.4 on 2022-05-22 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppJuegos', '0011_post_consola_delete_comentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='juego',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='AppJuegos.juego'),
        ),
    ]
