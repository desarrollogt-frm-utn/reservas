# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0029_especialidad_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='comision',
            name='codigo',
            field=models.PositiveIntegerField(null=True, blank=True, verbose_name='Código de comisión'),
        ),
    ]
