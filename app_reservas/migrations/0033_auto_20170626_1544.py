# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_reservas', '0032_auto_20170614_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateTimeField(verbose_name='Fecha de Creación')),
                ('asignado_por', models.ForeignKey(verbose_name='Asignado por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
        migrations.AlterModelOptions(
            name='docente',
            options={'verbose_name': 'Docente', 'verbose_name_plural': 'Docentes', 'ordering': ['nombre']},
        ),
        migrations.AlterField(
            model_name='horariosolicitud',
            name='tipoRecursoAli',
            field=models.ManyToManyField(verbose_name='Tipo de Recurso ALI', null=True, to='app_reservas.TipoRecursoAli', blank=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipoSolicitud',
            field=models.ForeignKey(verbose_name='Tipo de Solicitud', to='app_reservas.TipoSolicitud'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='horario',
            field=models.ForeignKey(verbose_name='Horario de Solicitud', to='app_reservas.HorarioSolicitud', related_name='reservas'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='recurso',
            field=models.ForeignKey(verbose_name='Solicitud', to='app_reservas.Recurso'),
        ),
    ]
