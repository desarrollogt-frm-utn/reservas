# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_parque_tecnologico', '0002_auto_20180217_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marca',
            name='descripcion',
            field=models.TextField(verbose_name='Descripciones', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='modificacion',
            name='detalle',
            field=models.TextField(verbose_name='Detalles', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(max_length=254, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='descripcion',
            field=models.TextField(verbose_name='Descripciones', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipocomponente',
            name='descripcion',
            field=models.TextField(verbose_name='Descripciones', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tiporecurso',
            name='descripcion',
            field=models.TextField(verbose_name='Descripciones', blank=True, null=True),
        ),
    ]
