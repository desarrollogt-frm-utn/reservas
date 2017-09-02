# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0036_auto_20170719_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoReserva',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=50, blank=True, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Estados de Reservas',
                'verbose_name': 'Estado de Reserva',
            },
        ),
        migrations.CreateModel(
            name='HistoricoEstadoReserva',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('fechaInicio', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fechaFin', models.DateTimeField(blank=True, verbose_name='Fecha de Fin', null=True)),
                ('descripcionCierre', models.CharField(max_length=150, verbose_name='Descripción de cierre de reserva')),
                ('estado', models.ForeignKey(to='app_reservas.EstadoReserva', verbose_name='Estado de la Reserva')),
            ],
            options={
                'ordering': ['fechaInicio'],
                'verbose_name_plural': 'Historicos de los Estados de las Reservas',
                'verbose_name': 'Historico del Estado de la Reserva',
            },
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='horario',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='nombreEvento',
        ),
        migrations.AddField(
            model_name='reserva',
            name='fechaFin',
            field=models.DateField(blank=True, verbose_name='Fecha de fin de reserva', null=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='fechaInicio',
            field=models.DateField(verbose_name='Fecha de inicio de reserva', default=datetime.datetime(2017, 8, 3, 21, 19, 35, 769552, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserva',
            name='nombreEvento',
            field=models.CharField(max_length=50, verbose_name='Nombre del evento', default='evento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicoestadoreserva',
            name='reserva',
            field=models.ForeignKey(to='app_reservas.Reserva', verbose_name='Reservas'),
        ),
    ]
