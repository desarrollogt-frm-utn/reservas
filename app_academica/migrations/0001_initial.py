# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_academica.models.comision
import app_academica.models.horario


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('comision', models.CharField(verbose_name='Comisión', max_length=10)),
                ('anioacademico', models.PositiveSmallIntegerField(verbose_name='Año Académico')),
                ('codigo', models.PositiveIntegerField(verbose_name='Código de comisión', blank=True, null=True)),
                ('cuatrimestre', app_academica.models.comision.CuatrimestreField(max_length=1, choices=[('0', 'Anual'), ('1', 'Primer Semestre'), ('2', 'Segundo Semestre')])),
            ],
            options={
                'verbose_name': 'Comision',
                'verbose_name_plural': 'Comisiones',
                'ordering': ['comision'],
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255, blank=True)),
                ('correo', models.EmailField(verbose_name='Correo', max_length=255, blank=True)),
                ('legajo', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Docente',
                'verbose_name_plural': 'Docentes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='DocenteComision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('grado', models.CharField(verbose_name='Grado', max_length=255, blank=True)),
                ('comision', models.ForeignKey(verbose_name='Comisión', related_name='docenteComision', to='app_academica.Comision')),
                ('docente', models.ForeignKey(verbose_name='Docente', to='app_academica.Docente')),
            ],
            options={
                'verbose_name': 'Docente de la comisión',
                'verbose_name_plural': 'Docentes de la comisión',
                'ordering': ['grado'],
            },
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255, blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripción', blank=True)),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo', blank=True, null=True)),
                ('visible', models.BooleanField(verbose_name='Visible en administración de aulas', default=False)),
            ],
            options={
                'verbose_name': 'Especialidad',
                'verbose_name_plural': 'Especialidades',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dia', app_academica.models.horario.DiasSemanaField(max_length=1, choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sabado')])),
                ('duracion', models.PositiveSmallIntegerField(verbose_name='Duración')),
                ('horaInicio', models.TimeField(verbose_name='Hora de Inicio')),
                ('comision', models.ForeignKey(verbose_name='Horario', to='app_academica.Comision')),
            ],
            options={
                'verbose_name': 'Horario de cursado',
                'verbose_name_plural': 'Horarios de cursado',
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255, blank=True)),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo', blank=True, null=True)),
                ('especialidad', models.ForeignKey(verbose_name='Especialidad', to='app_academica.Especialidad')),
            ],
            options={
                'verbose_name': 'Materia',
                'verbose_name_plural': 'Materias',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255, blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripción', blank=True)),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='materia',
            name='plan',
            field=models.ForeignKey(verbose_name='Plan', to='app_academica.Plan'),
        ),
        migrations.AddField(
            model_name='comision',
            name='materia',
            field=models.ForeignKey(verbose_name='Materia', to='app_academica.Materia'),
        ),
    ]
