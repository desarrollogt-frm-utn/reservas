# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0030_comision_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comision',
            name='comision',
            field=models.CharField(max_length=10, verbose_name='Comisión'),
        ),
    ]
