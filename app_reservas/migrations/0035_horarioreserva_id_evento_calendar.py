# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0034_auto_20180628_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='horarioreserva',
            name='id_evento_calendar',
            field=models.CharField(verbose_name='Id del evento', max_length=255, blank=True, null=True),
        ),
    ]
