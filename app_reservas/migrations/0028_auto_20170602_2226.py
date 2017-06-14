# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.solicitud
import app_reservas.models.comision
import app_reservas.models.horarioSolicitud
import app_reservas.models.horario


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0027_fields_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlumnoComision',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('legajo', models.PositiveIntegerField(verbose_name='Legajo')),
            ],
            options={
                'verbose_name_plural': 'Alumnos de la Comisión',
                'ordering': ['legajo'],
                'verbose_name': 'Alumno de la comisión',
            },
        ),
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('comision', models.CharField(max_length=5, verbose_name='Comisión')),
                ('anioacademico', models.PositiveSmallIntegerField(verbose_name='Año Académico')),
                ('cuatrimestre', app_reservas.models.comision.CuatrimestreField(choices=[('0', 'Anual'), ('1', 'Primer Semestre'), ('2', 'Segundo Semestre')], max_length=1)),
            ],
            options={
                'verbose_name_plural': 'Comisiones',
                'ordering': ['comision'],
                'verbose_name': 'Comision',
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('correo', models.EmailField(blank=True, max_length=50, verbose_name='Correo')),
                ('legajo', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'Docentes',
                'ordering': ['legajo'],
                'verbose_name': 'Docente',
            },
        ),
        migrations.CreateModel(
            name='DocenteComision',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('grado', models.CharField(blank=True, max_length=25, verbose_name='Grado')),
                ('comision', models.ForeignKey(related_name='docenteComision', to='app_reservas.Comision', verbose_name='Comisión')),
                ('docente', models.ForeignKey(to='app_reservas.Docente', verbose_name='Docente')),
            ],
            options={
                'verbose_name_plural': 'Docentes de la comisión',
                'ordering': ['grado'],
                'verbose_name': 'Docente de la comisión',
            },
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name_plural': 'Especialidades',
                'ordering': ['nombre'],
                'verbose_name': 'Especialidad',
            },
        ),
        migrations.CreateModel(
            name='EstadoSolicitud',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name_plural': 'Estados de solicitudes',
                'ordering': ['nombre'],
                'verbose_name': 'Estado de solicitud',
            },
        ),
        migrations.CreateModel(
            name='HistoricoEstadoSolicitud',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fechaInicio', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fechaFin', models.DateTimeField(blank=True, verbose_name='Fecha de Fin', null=True)),
                ('descripcionCierre', models.CharField(max_length=150, verbose_name='Descripción de cierre de solicitud')),
                ('estadoSolicitud', models.ForeignKey(to='app_reservas.EstadoSolicitud', verbose_name='Estado de la Solicitud')),
            ],
            options={
                'verbose_name_plural': 'Historicos de los Estados de las Solicitudes',
                'ordering': ['fechaInicio'],
                'verbose_name': 'Historico del Estado de la Solicitud',
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('dia', app_reservas.models.horario.DiasSemanaField(choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sabado')], max_length=1)),
                ('duracion', models.PositiveSmallIntegerField(verbose_name='Duración')),
                ('horaInicio', models.TimeField(verbose_name='Hora de Inicio')),
                ('comision', models.ForeignKey(to='app_reservas.Comision', verbose_name='Horario')),
            ],
            options={
                'verbose_name_plural': 'Horarios de cursado',
                'verbose_name': 'Horario de cursado',
            },
        ),
        migrations.CreateModel(
            name='HorarioSolicitud',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('dia', app_reservas.models.horarioSolicitud.DiasSemanaField(choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')], max_length=1)),
                ('duracion', models.PositiveSmallIntegerField(verbose_name='Duración')),
                ('horaInicio', models.TimeField(verbose_name='Hora de Inicio')),
            ],
            options={
                'verbose_name_plural': 'Horarios de la solicutud',
                'verbose_name': 'Horario de la solicitud',
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('codigo', models.CharField(max_length=5, verbose_name='Código')),
                ('especialidad', models.ForeignKey(to='app_reservas.Especialidad', verbose_name='Especialidad')),
            ],
            options={
                'verbose_name_plural': 'Materias',
                'ordering': ['codigo'],
                'verbose_name': 'Materia',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name_plural': 'Planes',
                'ordering': ['nombre'],
                'verbose_name': 'Plan',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(verbose_name='Fecha de Creación')),
                ('horaInicio', models.TimeField(verbose_name='Hora de Inicio')),
                ('horaFin', models.TimeField(verbose_name='Hora de Fin')),
                ('tipoRecurso', models.CharField(choices=[('1', 'Aula'), ('2', 'Laboratorio Informatico'), ('3', 'Laboratorio'), ('4', 'Recurso de ALI')], max_length=1)),
                ('comision', models.ForeignKey(to='app_reservas.Comision', blank=True, verbose_name='Comision', null=True)),
                ('docente', models.ForeignKey(to='app_reservas.Docente', verbose_name='Docente')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes',
                'ordering': ['fechaCreacion'],
                'verbose_name': 'Solicitud',
            },
        ),
        migrations.CreateModel(
            name='TipoSolicitud',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name_plural': 'Tipos de solicitudes',
                'ordering': ['nombre'],
                'verbose_name': 'Tipo de solicitud',
            },
        ),
        migrations.AddField(
            model_name='solicitud',
            name='tipoSolicitud',
            field=models.ForeignKey(to='app_reservas.TipoSolicitud', verbose_name='Tipo de la Solicitud'),
        ),
        migrations.AddField(
            model_name='materia',
            name='plan',
            field=models.ForeignKey(to='app_reservas.Plan', verbose_name='Plan'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='solicitud',
            field=models.ForeignKey(to='app_reservas.Solicitud', verbose_name='Horario de la solicitud'),
        ),
        migrations.AddField(
            model_name='historicoestadosolicitud',
            name='solicitud',
            field=models.ForeignKey(to='app_reservas.Solicitud', verbose_name='Solicitud'),
        ),
        migrations.AddField(
            model_name='comision',
            name='materia',
            field=models.ForeignKey(to='app_reservas.Materia', verbose_name='Materia'),
        ),
        migrations.AddField(
            model_name='alumnocomision',
            name='comision',
            field=models.ForeignKey(to='app_reservas.Comision', verbose_name='Comision'),
        ),
    ]
