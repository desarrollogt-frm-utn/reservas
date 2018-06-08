# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0028_auto_20180526_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedad',
            name='ancho_maximo',
            field=models.PositiveSmallIntegerField(verbose_name='Ancho máximo', blank=True, null=True, help_text='Ancho máximo del carrusel, medido en píxeles (px).'),
        ),
        migrations.AddField(
            model_name='novedad',
            name='color_fondo',
            field=models.CharField(verbose_name='Color de Fondo', max_length=50, default='white', help_text='Color de fondo que tendra la novedad.Debe estar en formato hexadecimal. Por ejemplo, un valor válido es: ."#ff8c0a"Por defecto es blanco'),
        ),
    ]
