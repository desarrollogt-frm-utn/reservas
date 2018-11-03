# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.BaseRecurso


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0033_recurso_sae_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseRecurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
                ('codigo', models.CharField(max_length=12, unique=True, default=app_reservas.models.BaseRecurso.obtener_codigo_aleatorio)),
            ],
            options={
                'verbose_name': 'Base del Recurso',
                'verbose_name_plural': 'Bases de los Recursos',
            },
        ),
        migrations.RemoveField(
            model_name='accesorio',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='accesorio',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='accesorio',
            name='id',
        ),
        migrations.AddField(
            model_name='accesorio',
            name='baserecurso_ptr',
            field=models.OneToOneField(primary_key=True, default=1, serialize=False, auto_created=True,
                                       parent_link=True, to='app_reservas.BaseRecurso'),
            preserve_default=False,
        ),
    ]
