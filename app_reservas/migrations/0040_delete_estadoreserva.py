# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0039_auto_20170807_1046'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EstadoReserva',
        ),
    ]
