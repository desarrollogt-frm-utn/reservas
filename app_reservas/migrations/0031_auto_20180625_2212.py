# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_reservas.models.historicoEstadoSolicitud
import app_reservas.models.horarioSolicitud
import app_reservas.models.historicoEstadoReserva
from django.conf import settings
import app_reservas.models.accesorio
import django.utils.timezone
import app_reservas.models.horarioReserva
import app_reservas.models.solicitud


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0002_auto_20180217_1504'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_reservas', '0030_auto_20180609_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accesorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('identificador', models.CharField(verbose_name='Nombre', max_length=255)),
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
            name='HistoricoEstadoReserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_inicio', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fecha_fin', models.DateTimeField(verbose_name='Fecha de Fin', blank=True, null=True)),
                ('descripcion_cierre', models.CharField(verbose_name='Descripción de cierre de reserva', max_length=150)),
                ('estado', app_reservas.models.historicoEstadoReserva.EstadoReservaField(max_length=1, choices=[('1', 'Activa'), ('2', 'Finalizada'), ('3', 'Dada de baja por usuario'), ('4', 'Dada de baja por bedel')])),
            ],
            options={
                'verbose_name': 'Historico del Estado de la Reserva',
                'verbose_name_plural': 'Historicos de los Estados de las Reservas',
                'ordering': ['fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='HistoricoEstadoSolicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_inicio', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fecha_fin', models.DateTimeField(verbose_name='Fecha de Fin', blank=True, null=True)),
                ('descripcion_cierre', models.CharField(verbose_name='Descripción de cierre de solicitud', max_length=150)),
                ('estado_solicitud', app_reservas.models.historicoEstadoSolicitud.EstadoSolicitudField(max_length=1, choices=[('1', 'Pendiente'), ('2', 'En curso'), ('3', 'Finalizada'), ('4', 'Dada de baja por usuario')])),
            ],
            options={
                'verbose_name': 'Historico del Estado de la Solicitud',
                'verbose_name_plural': 'Historicos de los Estados de las Solicitudes',
                'ordering': ['fecha_inicio'],
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
                ('tipo_recurso', app_reservas.models.horarioSolicitud.TipoRecursoField(max_length=1, choices=[('1', 'Aula'), ('2', 'Laboratorio Informatico'), ('3', 'Laboratorio'), ('4', 'Recurso de ALI')])),
                ('cantidad_alumnos', models.PositiveIntegerField(verbose_name='Cantidad de alumnos')),
                ('software_requerido', models.TextField(verbose_name='Software Requerido', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Horario de la solicitud',
                'verbose_name_plural': 'Horarios de la solicutud',
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
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio de reserva')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de fin de reserva', blank=True, null=True)),
                ('nombre_evento', models.CharField(verbose_name='Nombre del evento', max_length=150)),
                ('asignado_por', models.ForeignKey(verbose_name='Asignado por', to=settings.AUTH_USER_MODEL)),
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
                ('fecha_creacion', models.DateTimeField(verbose_name='Fecha de Creación')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio de solicitud')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de fin de solicitud', blank=True, null=True)),
                ('tipo_solicitud', app_reservas.models.solicitud.TipoSolicitudField(max_length=1, choices=[('1', 'Cursado Completo'), ('2', 'Cursado - Un solo día'), ('3', 'Fuera de Agenda - Periodo'), ('4', 'Fuera de Agenda - Un solo día')])),
                ('solicitante', models.ForeignKey(blank=True, null=True, related_name='solicutudes', to='app_usuarios.Usuario')),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
                'ordering': ['fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='TipoAccesorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255, blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripción', blank=True)),
            ],
            options={
                'verbose_name': 'Tipo de Accesorio',
                'verbose_name_plural': 'Tipo de Accesorios',
                'ordering': ['nombre'],
            },
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='nombre',
            field=models.CharField(verbose_name='Nombre', max_length=255),
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
            model_name='horariosolicitud',
            name='solicitud',
            field=models.ForeignKey(verbose_name='Solicitud', to='app_reservas.Solicitud'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='tipo_laboratorio',
            field=models.ForeignKey(verbose_name='Tipo de Laboratorio', blank=True, null=True, to='app_reservas.TipoLaboratorio'),
        ),
        migrations.AddField(
            model_name='horariosolicitud',
            name='tipo_recurso_ali',
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
            model_name='accesorioprestamo',
            name='prestamo',
            field=models.ForeignKey(verbose_name='Prestamo', related_name='prestamosAccesorios_all', to='app_reservas.Prestamo'),
        ),
        migrations.AddField(
            model_name='accesorio',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo', to='app_reservas.TipoAccesorio'),
        ),
        migrations.AddField(
            model_name='horarioreserva',
            name='id_evento_calendar',
            field=models.CharField(verbose_name='Id del evento', max_length=255, blank=True, null=True),
        ),
    ]
