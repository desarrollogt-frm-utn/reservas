# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0030_auto_20180609_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecursoSAE',
            fields=[
                ('recurso_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='app_reservas.Recurso')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=20, help_text='Nombre del recurso.')),
                ('slug', models.SlugField(verbose_name='Slug', help_text='Etiqueta corta que identifica al recurso, y sólo puede contener letras, números, guiones bajos y guiones medios. Generalmente es utilizada para las direcciones URL. Por ejemplo, si el nombre del tipo de recurso es "Cancha 01", un slug posible sería "chancha_01" o "cancha01".')),
            ],
            options={
                'verbose_name': 'Recurso de la SAE',
                'verbose_name_plural': 'Recursos de la SAE',
                'ordering': ['nombre'],
            },
            bases=('app_reservas.recurso',),
        ),
        migrations.CreateModel(
            name='TipoRecursoSAE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, help_text='Nombre del tipo de recurso, en singular.')),
                ('nombre_plural', models.CharField(verbose_name='Nombre en plural', max_length=50, help_text='Nombre del tipo de recurso, en plural.')),
                ('slug', models.SlugField(verbose_name='Slug', help_text='Etiqueta corta que identifica al tipo de recurso, y sólo puede contener letras, números, guiones bajos y guiones medios. Generalmente es utilizada para las direcciones URL. Por ejemplo, si el nombre del tipo de recurso es "Canchas de fútbol", un slug posible sería "canchas_futbol" o "canchas".')),
                ('is_visible_navbar', models.BooleanField(verbose_name='Visible en la navbar', default=False, help_text='Indica si el tipo de recurso se lista dentro de las opciones de SAE, en la navbar (barra de navegación superior) del sitio.')),
            ],
            options={
                'verbose_name': 'Tipo de recurso de la SAE',
                'verbose_name_plural': 'Tipos de recurso de la SAE',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='recursosae',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo', to='app_reservas.TipoRecursoSAE'),
        ),
    ]
