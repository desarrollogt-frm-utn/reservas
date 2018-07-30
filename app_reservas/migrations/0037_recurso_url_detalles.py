# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0036_auto_20180728_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurso',
            name='url_detalles',
            field=models.URLField(verbose_name='URL de detalles', max_length=400, blank=True, null=True, help_text='URL a la que se va a redirigir para obtener más info.Puede ser nulo.'),
        ),
    ]
