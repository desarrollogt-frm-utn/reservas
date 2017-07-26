# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0003_auto_20170718_2106'),
        ('app_reservas', '0034_auto_20170630_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='fechaFin',
            field=models.DateField(verbose_name='Fecha de fin de solicitud', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='fechaInicio',
            field=models.DateField(verbose_name='Fecha de inicio de solicitud', default=datetime.datetime(2017, 7, 19, 0, 6, 28, 77112, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitud',
            name='solicitante',
            field=models.ForeignKey(related_name='solicutudes', null=True, blank=True, to='app_usuarios.Docente'),
        ),
    ]
