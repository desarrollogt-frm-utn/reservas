# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
import app_reservas.models.horarioSolicitud


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0031_auto_20170607_2310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='horariosolicitud',
            old_name='horaInicio',
            new_name='inicio',
        ),
        migrations.RemoveField(
            model_name='horariosolicitud',
            name='duracion',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='horaFin',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='horaInicio',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='tipoRecurso',
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='cantidad_alumnos',
            field=models.PositiveIntegerField(default=0, verbose_name='Cantidad de alumnos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='fin',
            field=models.TimeField(default=datetime.datetime(2017, 6, 14, 15, 45, 41, 572837, tzinfo=utc), verbose_name='Hora de Fin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='softwareRequerido',
            field=models.TextField(blank=True, null=True, verbose_name='Software Requerido'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='tipoLaboratorio',
            field=models.ForeignKey(null=True, blank=True, to='app_reservas.TipoLaboratorio', verbose_name='Tipo de Laboratorio'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='tipoRecurso',
            field=app_reservas.models.horarioSolicitud.TipoRecursoField(choices=[('1', 'Aula'), ('2', 'Laboratorio Informatico'), ('3', 'Laboratorio'), ('4', 'Recurso de ALI')], max_length=1, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='tipoRecursoAli',
            field=models.ManyToManyField(to='app_reservas.TipoRecursoAli', verbose_name='Tipo de Recurso ALI'),
        ),
        migrations.AlterField(
            model_name='horariosolicitud',
            name='solicitud',
            field=models.ForeignKey(to='app_reservas.Solicitud', verbose_name='Solicitud'),
        ),
    ]
