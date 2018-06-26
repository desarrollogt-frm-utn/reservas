# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.recurso

import app_reservas.models.accesorio
from django.utils.crypto import get_random_string

def set_codigo(apps, schema_editor):
    recursos = apps.get_model("app_reservas", "recurso").objects.all()
    for recurso in recursos:
        random = get_random_string().upper()
        recurso.codigo = random
        recurso.save()

class Migration(migrations.Migration):


    dependencies = [
        ('app_reservas', '0031_auto_20180625_2212'),
    ]

    operations = [
        migrations.RunPython(set_codigo),
        migrations.AlterField(
            model_name='recurso',
            name='codigo',
            field=models.CharField(max_length=12, unique=True, default=app_reservas.models.recurso.obtener_codigo_aleatorio),
        ),
    ]
