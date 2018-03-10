# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.recurso
import django.utils.timezone
from django.conf import settings
import app_reservas.models.horario
import app_reservas.models.historicoEstadoReserva
import app_reservas.models.historicoEstadoSolicitud
import app_reservas.models.horarioSolicitud
import app_reservas.models.comision
import app_reservas.models.accesorio
import app_reservas.models.solicitud
import app_reservas.models.horarioReserva


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0002_auto_20180217_1504'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_reservas', '0027_fields_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accesorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('identificador', models.CharField(verbose_name='Nombre', max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('codigo', models.CharField(max_length=12, unique=True, default=app_reservas.models.accesorio.obtener_codigo_aleatorio)),
            ],
            options={
                'verbose_name': 'Accesorio',
                'verbose_name_plural': 'Accesorios',
            },
        ),
        migrations.CreateModel(
            name='AccesorioPrestamo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('accesorio', models.ForeignKey(verbose_name='Accesorio', related_name='accesorios_all', to='app_reservas.Accesorio')),
            ],
            options={
                'verbose_name': 'AccesorioPrestamo',
                'verbose_name_plural': 'AccesorioPrestamos',
            },
        ),
        migrations.CreateModel(
            name='AlumnoComision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('legajo', models.PositiveIntegerField(verbose_name='Legajo')),
            ],
            options={
                'verbose_name': 'Alumno de la comisión',
                'verbose_name_plural': 'Alumnos de la Comisión',
                'ordering': ['legajo'],
            },
        ),
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('comision', models.CharField(verbose_name='Comisión', max_length=10)),
                ('anioacademico', models.PositiveSmallIntegerField(verbose_name='Año Académico')),
                ('codigo', models.PositiveIntegerField(verbose_name='Código de comisión', blank=True, null=True)),
                ('cuatrimestre', app_reservas.models.comision.CuatrimestreField(max_length=1, choices=[('0', 'Anual'), ('1', 'Primer Semestre'), ('2', 'Segundo Semestre')])),
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
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, blank=True)),
                ('correo', models.EmailField(verbose_name='Correo', max_length=50, blank=True)),
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
                ('grado', models.CharField(verbose_name='Grado', max_length=25, blank=True)),
                ('comision', models.ForeignKey(verbose_name='Comisión', related_name='docenteComision', to='app_reservas.Comision')),
                ('docente', models.ForeignKey(verbose_name='Docente', to='app_reservas.Docente')),
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
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripción', blank=True)),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Especialidad',
                'verbose_name_plural': 'Especialidades',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='HistoricoEstadoReserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fechaInicio', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fechaFin', models.DateTimeField(verbose_name='Fecha de Fin', blank=True, null=True)),
                ('descripcionCierre', models.CharField(verbose_name='Descripción de cierre de reserva', max_length=150)),
                ('estado', app_reservas.models.historicoEstadoReserva.EstadoReservaField(max_length=1, choices=[('1', 'Activa'), ('2', 'Finalizada'), ('3', 'Dada de baja por usuario'), ('4', 'Dada de baja por bedel')])),
            ],
            options={
                'verbose_name': 'Historico del Estado de la Reserva',
                'verbose_name_plural': 'Historicos de los Estados de las Reservas',
                'ordering': ['fechaInicio'],
            },
        ),
        migrations.CreateModel(
            name='HistoricoEstadoSolicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fechaInicio', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fechaFin', models.DateTimeField(verbose_name='Fecha de Fin', blank=True, null=True)),
                ('descripcionCierre', models.CharField(verbose_name='Descripción de cierre de solicitud', max_length=150)),
                ('estadoSolicitud', app_reservas.models.historicoEstadoSolicitud.EstadoSolicitudField(max_length=1, choices=[('1', 'Pendiente'), ('2', 'En curso'), ('3', 'Finalizada'), ('4', 'Dada de baja por usuario')])),
            ],
            options={
                'verbose_name': 'Historico del Estado de la Solicitud',
                'verbose_name_plural': 'Historicos de los Estados de las Solicitudes',
                'ordering': ['fechaInicio'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dia', app_reservas.models.horario.DiasSemanaField(max_length=1, choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sabado')])),
                ('duracion', models.PositiveSmallIntegerField(verbose_name='Duración')),
                ('horaInicio', models.TimeField(verbose_name='Hora de Inicio')),
                ('comision', models.ForeignKey(verbose_name='Horario', to='app_reservas.Comision')),
            ],
            options={
                'verbose_name': 'Horario de cursado',
                'verbose_name_plural': 'Horarios de cursado',
            },
        ),
        migrations.CreateModel(
            name='HorarioReserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dia', app_reservas.models.horarioReserva.DiasSemanaField(max_length=1, choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')])),
                ('fin', models.TimeField(verbose_name='Hora de Fin')),
                ('inicio', models.TimeField(verbose_name='Hora de Inicio')),
            ],
            options={
                'verbose_name': 'Horario de la reserva',
                'verbose_name_plural': 'Horarios de la reserva',
            },
        ),
        migrations.CreateModel(
            name='HorarioSolicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dia', app_reservas.models.horarioSolicitud.DiasSemanaField(max_length=1, choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')])),
                ('fin', models.TimeField(verbose_name='Hora de Fin')),
                ('inicio', models.TimeField(verbose_name='Hora de Inicio')),
                ('tipoRecurso', app_reservas.models.horarioSolicitud.TipoRecursoField(max_length=1, choices=[('1', 'Aula'), ('2', 'Laboratorio Informatico'), ('3', 'Laboratorio'), ('4', 'Recurso de ALI')])),
                ('cantidad_alumnos', models.PositiveIntegerField(verbose_name='Cantidad de alumnos')),
                ('softwareRequerido', models.TextField(verbose_name='Software Requerido', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Horario de la solicitud',
                'verbose_name_plural': 'Horarios de la solicutud',
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, blank=True)),
                ('codigo', models.CharField(verbose_name='Código', max_length=5)),
                ('especialidad', models.ForeignKey(verbose_name='Especialidad', to='app_reservas.Especialidad')),
            ],
            options={
                'verbose_name': 'Materia',
                'verbose_name_plural': 'Materias',
                'ordering': ['codigo'],
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripción', blank=True)),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('inicio', models.DateTimeField(verbose_name='Inicio', default=django.utils.timezone.now)),
                ('fin', models.DateTimeField(verbose_name='Fin', blank=True, null=True)),
                ('asignado_por', models.ForeignKey(verbose_name='Asignado por', related_name='prestamos_asignados', to=settings.AUTH_USER_MODEL)),
                ('recibido_por', models.ForeignKey(verbose_name='Recibido por', blank=True, null=True, related_name='prestamos_recibidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Prestamo',
                'verbose_name_plural': 'Prestamos',
            },
        ),
        migrations.CreateModel(
            name='RecursoPrestamo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('prestamo', models.ForeignKey(verbose_name='Prestamo', related_name='recursos_all', to='app_reservas.Prestamo')),
            ],
            options={
                'verbose_name': 'RecursoPrestamo',
                'verbose_name_plural': 'RecursoPrestamos',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_creacion', models.DateTimeField(verbose_name='Fecha de Creación', default=django.utils.timezone.now)),
                ('fechaInicio', models.DateField(verbose_name='Fecha de inicio de reserva')),
                ('fechaFin', models.DateField(verbose_name='Fecha de fin de reserva', blank=True, null=True)),
                ('nombreEvento', models.CharField(verbose_name='Nombre del evento', max_length=150)),
                ('asignado_por', models.ForeignKey(verbose_name='Asignado por', to=settings.AUTH_USER_MODEL)),
                ('comision', models.ForeignKey(verbose_name='Comision', blank=True, null=True, to='app_reservas.Comision')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fechaCreacion', models.DateTimeField(verbose_name='Fecha de Creación')),
                ('fechaInicio', models.DateField(verbose_name='Fecha de inicio de solicitud')),
                ('fechaFin', models.DateField(verbose_name='Fecha de fin de solicitud', blank=True, null=True)),
                ('tipoSolicitud', app_reservas.models.solicitud.TipoSolicitudField(max_length=1, choices=[('1', 'Cursado Completo'), ('2', 'Cursado - Un solo día'), ('3', 'Fuera de Horario - Periodo'), ('4', 'Fuera de Horario - Un solo día')])),
                ('comision', models.ForeignKey(verbose_name='Comision', blank=True, null=True, to='app_reservas.Comision')),
                ('docente', models.ForeignKey(verbose_name='Docente', to='app_reservas.Docente')),
                ('solicitante', models.ForeignKey(blank=True, null=True, related_name='solicutudes', to='app_usuarios.Usuario')),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
                'ordering': ['fechaCreacion'],
            },
        ),
        migrations.CreateModel(
            name='TipoAccesorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripción', blank=True)),
            ],
            options={
                'verbose_name': 'Tipo de Accesorio',
                'verbose_name_plural': 'Tipo de Accesorios',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='recurso',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='recurso',
            name='codigo',
            field=models.CharField(max_length=12, blank=True, null=True,),
        ),
        migrations.AddField(
            model_name='reserva',
            name='recurso',
            field=models.ForeignKey(verbose_name='Recurso de la Reserva', to='app_reservas.Recurso'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, related_name='reservas', to='app_usuarios.Usuario'),
        ),
        migrations.AddField(
            model_name='recursoprestamo',
            name='recurso',
            field=models.ForeignKey(verbose_name='Recurso', related_name='prestamos_all', to='app_reservas.Recurso'),
        ),
        migrations.AddField(
            model_name='recursoprestamo',
            name='reserva',
            field=models.ForeignKey(verbose_name='Reserva', related_name='reservas_all', to='app_reservas.Reserva'),
        ),
        migrations.AddField(
            model_name='materia',
            name='plan',
            field=models.ForeignKey(verbose_name='Plan', to='app_reservas.Plan'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='solicitud',
            field=models.ForeignKey(verbose_name='Solicitud', to='app_reservas.Solicitud'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='tipoLaboratorio',
            field=models.ForeignKey(verbose_name='Tipo de Laboratorio', blank=True, null=True, to='app_reservas.TipoLaboratorio'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='tipoRecursoAli',
            field=models.ManyToManyField(verbose_name='Tipo de Recurso ALI', blank=True, to='app_reservas.TipoRecursoAli'),
        ),
        migrations.AddField(
            model_name='horarioreserva',
            name='reserva',
            field=models.ForeignKey(verbose_name='Reserva', blank=True, null=True, to='app_reservas.Reserva'),
        ),
        migrations.AddField(
            model_name='historicoestadosolicitud',
            name='solicitud',
            field=models.ForeignKey(verbose_name='Solicitud', to='app_reservas.Solicitud'),
        ),
        migrations.AddField(
            model_name='historicoestadoreserva',
            name='reserva',
            field=models.ForeignKey(verbose_name='Reservas', to='app_reservas.Reserva'),
        ),
        migrations.AddField(
            model_name='comision',
            name='materia',
            field=models.ForeignKey(verbose_name='Materia', to='app_reservas.Materia'),
        ),
        migrations.AddField(
            model_name='alumnocomision',
            name='comision',
            field=models.ForeignKey(verbose_name='Comision', to='app_reservas.Comision'),
        ),
        migrations.AddField(
            model_name='accesorioprestamo',
            name='prestamo',
            field=models.ForeignKey(verbose_name='Prestamo', related_name='prestamosAccesorios_all', to='app_reservas.Prestamo'),
        ),
        migrations.AddField(
            model_name='accesorio',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo', to='app_reservas.TipoAccesorio'),
        ),
    ]
