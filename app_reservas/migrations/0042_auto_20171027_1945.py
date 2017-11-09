# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.historicoEstadoSolicitud


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0041_horarioreserva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoestadosolicitud',
            name='estadoSolicitud',
            field=app_reservas.models.historicoEstadoSolicitud.EstadoSolicitudField(max_length=1, choices=[('1', 'Pendiente'), ('2', 'En curso'), ('3', 'Finalizada')]),
        ),
        migrations.DeleteModel(
            name='EstadoSolicitud',
        ),
    ]
