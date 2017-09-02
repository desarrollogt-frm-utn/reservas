# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0002_auto_20170710_1916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='docente',
            options={'verbose_name': 'Docente', 'ordering': ['email'], 'verbose_name_plural': 'Docentes'},
        ),
    ]
