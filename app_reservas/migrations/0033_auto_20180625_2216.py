# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_academica', '0001_initial'),
        ('app_reservas', '0032_auto_20180303_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='comision',
            field=models.ForeignKey(verbose_name='Comision', blank=True, null=True, to='app_academica.Comision'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='comision',
            field=models.ForeignKey(verbose_name='Comision', blank=True, null=True, to='app_academica.Comision'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='docente',
            field=models.ForeignKey(verbose_name='Docente', default=1, to='app_academica.Docente'),
            preserve_default=False,
        ),
    ]
