# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0037_prestamo_recurso_base'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoAula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, help_text='Nombre del tipo de aula, en singular.')),
                ('nombre_plural', models.CharField(verbose_name='Nombre en plural', max_length=50, help_text='Nombre del tipo de aula, en plural.')),
                ('slug', models.SlugField(verbose_name='Slug', help_text='Etiqueta corta que identifica al tipo de aulas, y sólo puede contener letras, números, guiones bajos y guiones medios. Generalmente es utilizada para las direcciones URL. Por ejemplo, si el nombre del tipo de aula es "Aulas Multimedia", un slug posible sería "aulas_multimedia" o "multimedia".')),
                ('is_visible_navbar', models.BooleanField(verbose_name='Visible en la navbar', default=False, help_text='Indica si el tipo de recurso se lista dentro de las opciones de Aulas, en la navbar (barra de navegación superior) del sitio.')),
            ],
            options={
                'verbose_name': 'Tipo de Aula',
                'verbose_name_plural': 'Tipos de Aula',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='TipoRecursoUM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=50, help_text='Nombre del tipo de recurso, en singular.')),
                ('nombre_plural', models.CharField(verbose_name='Nombre en plural', max_length=50, help_text='Nombre del tipo de recurso, en plural.')),
                ('slug', models.SlugField(verbose_name='Slug', help_text='Etiqueta corta que identifica al tipo de recurso, y sólo puede contener letras, números, guiones bajos y guiones medios. Generalmente es utilizada para las direcciones URL. Por ejemplo, si el nombre del tipo de recurso es "Canchas de fútbol", un slug posible sería "canchas_futbol" o "canchas".')),
                ('is_visible_navbar', models.BooleanField(verbose_name='Visible en la navbar', default=False, help_text='Indica si el tipo de recurso se lista dentro de las opciones de SAE, en la navbar (barra de navegación superior) del sitio.')),
            ],
            options={
                'verbose_name': 'Tipo de recurso de usos múltiple',
                'verbose_name_plural': 'Tipos de recurso de usos múltiple',
                'ordering': ['nombre'],
            },
        ),
        migrations.RenameModel(
            old_name='RecursoSAE',
            new_name='RecursoUM',
        ),
        migrations.DeleteModel(
            name='TipoRecursoSAE',
        ),
        migrations.AlterModelOptions(
            name='recursoum',
            options={'verbose_name': 'Recurso de Usos Múltiples', 'verbose_name_plural': 'Recursos de Usos Múltiples', 'ordering': ['nombre']},
        ),
        migrations.AlterField(
            model_name='recursoum',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo', to='app_reservas.TipoRecursoUM'),
        ),
        migrations.AddField(
            model_name='aula',
            name='tipo',
            field=models.ManyToManyField(verbose_name='Tipo de Aula', to='app_reservas.TipoAula'),
        ),
    ]
