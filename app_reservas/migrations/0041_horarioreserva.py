# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.horarioReserva


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0040_delete_estadoreserva'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorarioReserva',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('dia', app_reservas.models.horarioReserva.DiasSemanaField(max_length=1, choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')])),
                ('fin', models.TimeField(verbose_name='Hora de Fin')),
                ('inicio', models.TimeField(verbose_name='Hora de Inicio')),
                ('reserva', models.ForeignKey(to='app_reservas.Reserva', blank=True, verbose_name='Reserva', null=True)),
            ],
            options={
                'verbose_name': 'Horario de la reserva',
                'verbose_name_plural': 'Horarios de la reserva',
            },
        ),
    ]
