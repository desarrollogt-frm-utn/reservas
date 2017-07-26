# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.solicitud


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0035_auto_20170718_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='nombreEvento',
            field=models.CharField(null=True, max_length=50, blank=True, verbose_name='Nombre del evento'),
        ),
        migrations.AlterField(
            model_name='horariosolicitud',
            name='tipoRecursoAli',
            field=models.ManyToManyField(to='app_reservas.TipoRecursoAli', blank=True, verbose_name='Tipo de Recurso ALI'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipoSolicitud',
            field=app_reservas.models.solicitud.TipoSolicitudField(max_length=1, choices=[('1', 'Cursado Completo'), ('2', 'Cursado - Un solo día'), ('3', 'Fuera de Horario - Periodo'), ('4', 'Fuera de Horario - Un solo día')]),
        ),
        migrations.DeleteModel(
            name='TipoSolicitud',
        ),
    ]
