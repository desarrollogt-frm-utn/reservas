# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0036_recurso_pk_fix'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesorioprestamo',
            name='accesorio',
        ),
        migrations.RemoveField(
            model_name='accesorioprestamo',
            name='prestamo',
        ),
        migrations.AlterField(
            model_name='recursoprestamo',
            name='recurso',
            field=models.ForeignKey(verbose_name='Recurso', related_name='prestamos_all', to='app_reservas.BaseRecurso'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='recurso',
            field=models.ForeignKey(verbose_name='Recurso de la Reserva', to='app_reservas.BaseRecurso'),
        ),
        migrations.DeleteModel(
            name='AccesorioPrestamo',
        ),
    ]
