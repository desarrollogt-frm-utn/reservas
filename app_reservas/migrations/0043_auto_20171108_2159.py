# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import app_reservas.models.recurso
import app_reservas.models.accesorio
from django.utils.crypto import get_random_string


def set_codigo(apps, schema_editor):
    recursos = apps.get_model("app_reservas", "recurso").objects.all()
    for recurso in recursos:
        random = get_random_string().upper()
        recurso.codigo = random
        recurso.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_reservas', '0042_auto_20171027_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accesorio',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('identificador', models.CharField(verbose_name='Nombre', max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('codigo', models.CharField(default=app_reservas.models.accesorio.obtener_codigo_aleatorio, unique=True, max_length=12)),
            ],
            options={
                'verbose_name': 'Accesorio',
                'verbose_name_plural': 'Accesorios',
            },
        ),
        migrations.CreateModel(
            name='AccesorioPrestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('accesorio', models.ForeignKey(verbose_name='Recurso', related_name='accesorios_all', to='app_reservas.Accesorio')),
            ],
            options={
                'verbose_name': 'AccesorioPrestamo',
                'verbose_name_plural': 'AccesorioPrestamos',
            },
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('inicio', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fin', models.DateTimeField(verbose_name='Fecha de Fin', null=True, blank=True)),
                ('asignado_por', models.ForeignKey(verbose_name='Asignado por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Prestamo',
                'verbose_name_plural': 'Prestamos',
            },
        ),
        migrations.CreateModel(
            name='RecursoPrestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('prestamo', models.ForeignKey(verbose_name='Prestamo', related_name='recursos_all', to='app_reservas.Prestamo')),
            ],
            options={
                'verbose_name': 'RecursoPrestamo',
                'verbose_name_plural': 'RecursoPrestamos',
            },
        ),
        migrations.CreateModel(
            name='TipoAccesorio',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripción', blank=True)),
            ],
            options={
                'verbose_name': 'Tipo de Accesorio',
                'ordering': ['nombre'],
                'verbose_name_plural': 'Tipo de Accesorios',
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
            field=models.CharField(max_length=12, null=True, blank=True),
        ),
        migrations.RunPython(set_codigo),
        migrations.AlterField(
            model_name='recurso',
            name='codigo',
            field=models.CharField(unique=True, max_length=12, null=False, blank=False),
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
