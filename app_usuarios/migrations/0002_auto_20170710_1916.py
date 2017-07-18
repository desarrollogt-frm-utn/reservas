# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='docente',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='docente',
            name='id',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='user',
        ),
        migrations.AddField(
            model_name='docente',
            name='user_ptr',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, default=1, auto_created=True, serialize=False, parent_link=True, primary_key=True),
            preserve_default=False,
        ),
    ]
