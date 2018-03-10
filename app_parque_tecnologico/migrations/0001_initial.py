# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_usuarios', '0001_initial'),
        ('app_reservas', '0027_fields_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('capacidad', models.CharField(max_length=10)),
                ('modelo', models.CharField(max_length=25)),
                ('nro_serie', models.CharField(max_length=30)),
                ('MAC', models.CharField(max_length=17)),
            ],
            options={
                'verbose_name': 'Componente',
                'verbose_name_plural': 'Componentes',
            },
        ),
        migrations.CreateModel(
            name='Garantia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_compra', models.DateField()),
                ('fecha_expiracion', models.DateField()),
                ('nro_factura', models.PositiveIntegerField()),
                ('valor', models.DecimalField(max_digits=14, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Garantia',
                'verbose_name_plural': 'Garantias',
            },
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nro_local', models.PositiveIntegerField()),
                ('nivel', models.ForeignKey(to='app_reservas.Nivel')),
            ],
            options={
                'verbose_name': 'Local',
                'verbose_name_plural': 'Locales',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
            },
        ),
        migrations.CreateModel(
            name='Modificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha', models.DateTimeField()),
                ('detalle', models.CharField(max_length=100)),
                ('autor', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('componente', models.ForeignKey(to='app_parque_tecnologico.Componente')),
            ],
            options={
                'verbose_name': 'Modificación',
                'verbose_name_plural': 'Modificaciones',
            },
        ),
        migrations.CreateModel(
            name='Patrimonial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('id_patrimonial', models.PositiveIntegerField()),
                ('nro_expediente', models.CharField(max_length=12)),
                ('responsable', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Patrimonial',
                'verbose_name_plural': 'Patrimoniales',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedor',
            },
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=10, unique=True)),
                ('fecha_alta', models.DateTimeField(verbose_name='Fecha de Alta')),
                ('observaciones', models.CharField(verbose_name='Observaciones', max_length=100)),
                ('nro_incidente', models.PositiveIntegerField()),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('garantia', models.OneToOneField(blank=True, null=True, to='app_parque_tecnologico.Garantia')),
                ('patrimonial', models.OneToOneField(blank=True, null=True, to='app_parque_tecnologico.Patrimonial')),
            ],
            options={
                'verbose_name': 'Recurso',
                'verbose_name_plural': 'Recursos',
            },
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
                ('interno', models.PositiveIntegerField()),
                ('descripcion', models.CharField(max_length=50)),
                ('area', models.ForeignKey(to='app_reservas.Area')),
            ],
            options={
                'verbose_name': 'Sección',
                'verbose_name_plural': 'Secciones',
            },
        ),
        migrations.CreateModel(
            name='TipoComponente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tipo de Componete',
                'verbose_name_plural': 'Tipos de Componentes',
            },
        ),
        migrations.CreateModel(
            name='TipoRecurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
                ('identificacion', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tipo de Recurso',
                'verbose_name_plural': 'Tipos de Recursos',
            },
        ),
        migrations.CreateModel(
            name='Trazabilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('local', models.ForeignKey(to='app_parque_tecnologico.Local')),
                ('recurso', models.ForeignKey(related_name='trazabilidades', to='app_parque_tecnologico.Recurso')),
                ('seccion', models.ForeignKey(to='app_parque_tecnologico.Seccion')),
                ('usuario', models.OneToOneField(to='app_usuarios.Usuario')),
            ],
            options={
                'verbose_name': 'Trazabilidad',
                'verbose_name_plural': 'Trazabilidades',
            },
        ),
        migrations.AddField(
            model_name='recurso',
            name='tipo_recurso',
            field=models.ForeignKey(to='app_parque_tecnologico.TipoRecurso'),
        ),
        migrations.AddField(
            model_name='modificacion',
            name='recurso',
            field=models.ForeignKey(related_name='modificaciones', to='app_parque_tecnologico.Recurso'),
        ),
        migrations.AddField(
            model_name='componente',
            name='garantia',
            field=models.OneToOneField(blank=True, null=True, to='app_parque_tecnologico.Garantia'),
        ),
        migrations.AddField(
            model_name='componente',
            name='marca',
            field=models.ForeignKey(to='app_parque_tecnologico.Marca'),
        ),
        migrations.AddField(
            model_name='componente',
            name='proveedor',
            field=models.ForeignKey(to='app_parque_tecnologico.Proveedor'),
        ),
        migrations.AddField(
            model_name='componente',
            name='recurso',
            field=models.ForeignKey(blank=True, null=True, related_name='componente', to='app_parque_tecnologico.Recurso'),
        ),
        migrations.AddField(
            model_name='componente',
            name='tipo_componente',
            field=models.ForeignKey(to='app_parque_tecnologico.TipoComponente'),
        ),
    ]
