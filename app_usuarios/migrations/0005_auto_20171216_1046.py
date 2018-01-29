# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0004_docente_celular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docente',
            name='legajo',
            field=models.PositiveIntegerField(default=1, unique=True),
        ),
    ]
