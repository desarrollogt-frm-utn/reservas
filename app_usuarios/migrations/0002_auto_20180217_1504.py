# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='celular',
            field=models.CharField(verbose_name='celular', max_length=30, blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?[\\d()*-]+$', message='El formato de número de teléfono es incorrecto.')]),
        ),
    ]
