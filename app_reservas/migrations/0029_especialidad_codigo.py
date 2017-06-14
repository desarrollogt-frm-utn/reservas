# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0028_auto_20170602_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialidad',
            name='codigo',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Codigo'),
        ),
    ]
