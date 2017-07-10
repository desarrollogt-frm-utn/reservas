# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0033_auto_20170626_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='recurso',
            field=models.ForeignKey(verbose_name='Recurso de la Reserva', to='app_reservas.Recurso'),
        ),
    ]
