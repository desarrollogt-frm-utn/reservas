# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0027_fields_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Novedad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('texto_principal', models.TextField(verbose_name='Texto de la novedad', blank=True, null=True, help_text='Texto en formato html que será mostrado en las pantallas de novedades')),
                ('texto_pie_pagina', models.CharField(verbose_name='Texto del pie', max_length=255, blank=True, null=True, help_text='Texto que aparecerá en el pie de la página. Puede contener hasta 255 caracteres')),
                ('slug', models.SlugField(verbose_name='Slug', unique=True, help_text='Etiqueta corta que identifica a la novedad carrusel, y sólo puede contener letras, números, guiones bajos y guiones medios.')),
                ('carrusel', models.ForeignKey(verbose_name='Carrusel', blank=True, null=True, help_text='Carrusel de imagenes que será mostrado. En caso de ser nulo se mostrará el campo Texto Principal', related_name='novedades', to='app_reservas.CarruselImagenes')),
            ],
            options={
                'verbose_name': 'Novedad',
                'verbose_name_plural': 'Novedades',
            },
        ),
        migrations.AddField(
            model_name='visortv',
            name='texto_pie_pagina',
            field=models.CharField(verbose_name='Texto del pie', max_length=255, blank=True, null=True, help_text='Texto que aparecerá en el pie de la página. Puede contener hasta 255 caracteres'),
        ),
    ]
