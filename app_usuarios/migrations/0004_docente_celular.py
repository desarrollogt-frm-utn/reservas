# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0003_auto_20170718_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='celular',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='El formato de número de teléfono es incorrecto.', regex='^\\+?[\\d()*-]+$')], max_length=30, default=123, verbose_name='celular'),
            preserve_default=False,
        ),
    ]
