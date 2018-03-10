# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_parque_tecnologico', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurso',
            name='nro_incidente',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recurso',
            name='observaciones',
            field=models.TextField(verbose_name='Observaciones', blank=True, null=True),
        ),
    ]
