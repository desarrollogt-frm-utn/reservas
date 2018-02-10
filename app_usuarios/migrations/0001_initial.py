# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import app_usuarios.models
import django.contrib.auth.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('legajo', models.PositiveIntegerField(unique=True)),
                ('telefono', models.CharField(verbose_name='teléfono', max_length=30, blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?[\\d()*-]+$', message='El formato de número de teléfono es incorrecto.')])),
                ('celular', models.CharField(verbose_name='celular', max_length=30, validators=[django.core.validators.RegexValidator(regex='^\\+?[\\d()*-]+$', message='El formato de número de teléfono es incorrecto.')])),
                ('foto', models.ImageField(blank=True, null=True, upload_to=app_usuarios.models.establecer_destino_archivo_imagen)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'ordering': ['email'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
