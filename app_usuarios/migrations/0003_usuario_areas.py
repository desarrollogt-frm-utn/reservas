# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0030_auto_20180609_1429'),
        ('app_usuarios', '0002_auto_20180217_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='areas',
            field=models.ManyToManyField(verbose_name='Áreas', blank=True, null=True, to='app_reservas.Area'),
        ),
    ]
