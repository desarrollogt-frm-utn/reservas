# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0003_usuario_areas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='areas',
            field=models.ManyToManyField(verbose_name='Áreas', blank=True, to='app_reservas.Area'),
        ),
    ]
