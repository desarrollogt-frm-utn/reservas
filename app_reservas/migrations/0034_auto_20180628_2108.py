# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_academica', '0001_initial'),
        ('app_reservas', '0033_auto_20180625_2216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserva',
            old_name='fechaFin',
            new_name='fecha_fin',
        ),
        migrations.RenameField(
            model_name='reserva',
            old_name='fechaInicio',
            new_name='fecha_inicio',
        ),
        migrations.RenameField(
            model_name='reserva',
            old_name='nombreEvento',
            new_name='nombre_evento',
        ),
        migrations.AddField(
            model_name='reserva',
            name='docente',
            field=models.ForeignKey(verbose_name='Docente', default=1, to='app_academica.Docente'),
            preserve_default=False,
        ),
    ]
