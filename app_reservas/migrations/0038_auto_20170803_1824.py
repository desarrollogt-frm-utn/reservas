# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0003_auto_20170718_2106'),
        ('app_reservas', '0037_auto_20170803_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='comision',
            field=models.ForeignKey(to='app_reservas.Comision', null=True, verbose_name='Comision', blank=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='docente',
            field=models.ForeignKey(to='app_usuarios.Docente', null=True, related_name='reservas', blank=True),
        ),
    ]
