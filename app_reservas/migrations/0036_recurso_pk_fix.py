# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.crypto import get_random_string

class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0035_recurso_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurso',
            name='id',
        ),
        migrations.AlterField(
            model_name='recurso',
            name='baserecurso_ptr',
            field=models.OneToOneField(primary_key=True, serialize=False, auto_created=True,
                                       parent_link=True, to='app_reservas.BaseRecurso'),
            preserve_default=False,
        ),

    ]
