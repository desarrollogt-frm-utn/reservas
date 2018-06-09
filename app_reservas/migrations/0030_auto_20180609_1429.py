# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.imagenContingencia


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0029_auto_20180608_0212'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenContingencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('imagen', models.ImageField(verbose_name='Imagen', help_text='Archivo de imagen.', upload_to=app_reservas.models.imagenContingencia.establecer_destino_archivo_imagen)),
                ('activo', models.BooleanField(verbose_name='Imagen Activa', default=False, help_text='Indica si la imagen de contingencia se encuentra activa. Solo puede haber una activa al mismo tiempo.')),
                ('descripcion', models.CharField(verbose_name='Descripción', max_length=50, blank=True, help_text='Descripción de la imagen')),
            ],
            options={
                'verbose_name': 'Imagen de contingencia',
                'verbose_name_plural': 'Imágenes de contingencia',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='novedad',
            name='tiempo_actualizacion',
            field=models.PositiveSmallIntegerField(verbose_name='Tiempo de Actualización', default=300, help_text='Periodo que determina cada cuanto tiempo se actualizará la página medido en segundo.Por defecto es 300 segundos.'),
        ),
    ]
