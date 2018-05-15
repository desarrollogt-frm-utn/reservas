# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0029_auto_20180303_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesorio',
            name='identificador',
            field=models.CharField(verbose_name='Nombre', max_length=255),
        ),
        migrations.AlterField(
            model_name='docente',
            name='correo',
            field=models.EmailField(verbose_name='Correo', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='docente',
            name='nombre',
            field=models.CharField(verbose_name='Nombre', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='docentecomision',
            name='grado',
            field=models.CharField(verbose_name='Grado', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='nombre',
            field=models.CharField(verbose_name='Nombre', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='nombre',
            field=models.CharField(verbose_name='Nombre', max_length=255),
        ),
        migrations.AlterField(
            model_name='materia',
            name='codigo',
            field=models.PositiveIntegerField(verbose_name='Codigo', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='materia',
            name='nombre',
            field=models.CharField(verbose_name='Nombre', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='nombre',
            field=models.CharField(verbose_name='Nombre', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='tipoaccesorio',
            name='nombre',
            field=models.CharField(verbose_name='Nombre', max_length=255, blank=True),
        ),
        migrations.AlterModelOptions(
            name='materia',
            options={'verbose_name': 'Materia', 'verbose_name_plural': 'Materias', 'ordering': ['nombre']},
        ),
        migrations.AddField(
            model_name='especialidad',
            name='visible',
            field=models.BooleanField(verbose_name='Visible en administración de aulas', default=False),
        ),
    ]
