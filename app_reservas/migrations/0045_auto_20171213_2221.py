# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0044_auto_20171118_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha_creacion',
            field=models.DateTimeField(verbose_name='Fecha de Creación', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='nombreEvento',
            field=models.CharField(verbose_name='Nombre del evento', max_length=150),
        ),
    ]
