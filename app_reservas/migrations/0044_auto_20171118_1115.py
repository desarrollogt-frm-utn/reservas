# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.recurso
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_reservas', '0043_auto_20171108_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='recibido_por',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='prestamos_recibidos', verbose_name='Recibido por'),
        ),
        migrations.AlterField(
            model_name='accesorioprestamo',
            name='accesorio',
            field=models.ForeignKey(to='app_reservas.Accesorio', verbose_name='Accesorio', related_name='accesorios_all'),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='asignado_por',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Asignado por', related_name='prestamos_asignados'),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fin',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Fin'),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Inicio'),
        ),
        migrations.AlterField(
            model_name='recurso',
            name='codigo',
            field=models.CharField(default=app_reservas.models.recurso.obtener_codigo_aleatorio, unique=True, max_length=12),
        ),
    ]
