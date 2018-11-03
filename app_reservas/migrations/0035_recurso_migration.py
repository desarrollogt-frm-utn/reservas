# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.crypto import get_random_string


def migrate_recursos(apps, schema_editor):
    base_recurso_model = apps.get_model("app_reservas", "BaseRecurso")
    # recurso_models_names = ["Aula", "Laboratorio", "LaboratorioInformatico", "RecursoALI"]
    recurso_models_names = ["recurso"]
    for model_name in recurso_models_names:
        recurso_model = apps.get_model("app_reservas", model_name)

        for recurso in recurso_model.objects.all():
            base_recurso = base_recurso_model()
            base_recurso.codigo = get_random_string().upper()
            base_recurso.id = recurso.id

            recurso.baserecurso_ptr_id = base_recurso.id
            recurso.baserecurso_ptr = base_recurso
            base_recurso.save()
            recurso.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app_reservas', '0034_base_recurso'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurso',
            name='baserecurso_ptr',
            field=models.OneToOneField(null=True, serialize=False, auto_created=True, parent_link=True, to='app_reservas.BaseRecurso'),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_recursos),
        migrations.AddField(
            model_name='recurso',
            name='url_detalles',
            field=models.URLField(verbose_name='URL de detalles', max_length=400, blank=True, null=True,
                                  help_text='URL a la que se va a redirigir para obtener más info.Puede ser nulo.'),
        ),
    ]
