# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.historicoEstadoReserva


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0038_auto_20170803_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoestadoreserva',
            name='estado',
            field=app_reservas.models.historicoEstadoReserva.EstadoReservaField(choices=[('1', 'Activa'), ('2', 'Finalizada'), ('3', 'Dada de baja por usuario'), ('4', 'Dada de baja por bedel')], max_length=1),
        ),
    ]
