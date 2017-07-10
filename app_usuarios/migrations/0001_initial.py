# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import app_usuarios.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('legajo', models.PositiveIntegerField(default=1)),
                ('telefono', models.CharField(validators=[django.core.validators.RegexValidator(regex='^\\+?[\\d()*-]+$', message='El formato de número de teléfono es incorrecto.')], max_length=30, verbose_name='teléfono', null=True, blank=True)),
                ('foto', models.ImageField(null=True, upload_to=app_usuarios.models.establecer_destino_archivo_imagen, blank=True)),
                ('user', models.OneToOneField(related_name='docente', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Docente',
                'verbose_name_plural': 'Docentes',
                'ordering': ['user__username'],
            },
        ),
    ]
