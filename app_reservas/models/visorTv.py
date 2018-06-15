# coding=utf-8

from django.db import models

from ..services.recursos import (
    get_recursos_asociados,
    get_recursos_asociados_por_cuerpo,
)


class VisorTv(models.Model):
    # Atributos
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug',
        help_text='Etiqueta corta que identifica al visor de TV, y sólo puede contener '
                  'letras, números, guiones bajos y guiones medios. Generalmente es utilizada '
                  'para las direcciones URL. Por ejemplo, si el nombre del visor de TV es '
                  '"Departamento de Sistemas", un slug posible sería "sistemas" o '
                  '"departamento_sistemas".',
    )
    texto_pie_pagina = models.CharField(
        verbose_name='Texto del pie',
        blank=True,
        null=True,
        max_length=255,
        help_text='Texto que aparecerá en el pie de la página. Puede contener hasta 255 caracteres',
    )
    # Relaciones
    area = models.ForeignKey(
        'Area',
        verbose_name='Área',
    )
    aulas = models.ManyToManyField(
        'Aula',
        blank=True,
        verbose_name='Aulas',
    )
    laboratorios = models.ManyToManyField(
        'Laboratorio',
        blank=True,
        verbose_name='Laboratorios de Ingeniería',
    )
    laboratorios_informatica = models.ManyToManyField(
        'LaboratorioInformatico',
        blank=True,
        verbose_name='Laboratorios de Informática',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Visor de TV'
        verbose_name_plural = 'Visores de TV'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return 'Visor de TV: {0!s}'.format(self.nombre)

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        return self.nombre

    def get_aulas(self):
        """
        Retorna el listado de aulas asociadas a la instancia.
        """
        return self.aulas.all()

    def get_laboratorios(self):
        """
        Retorna el listado de laboratorios asociados a la instancia.
        """
        return self.laboratorios.all()

    def get_laboratorios_informatica(self):
        """
        Retorna el listado de laboratorios informáticos asociados a la instancia.
        """
        return self.laboratorios_informatica.all()

    def get_recursos(self):
        """
        Retorna todos los recursos asociados a la instancia.

        Returns
        -------
        list of dicts
            Lista de diccionarios, uno por cada tipo de recurso asociado que presenta al menos una
            instancia relacionada.
        """
        return get_recursos_asociados(self)

    def get_recursos_por_cuerpo(self):
        """
        Retorna todos los recursos asociados a la instancia, separados por cuerpo.

        Returns
        -------
        list of dicts
            Lista de diccionarios, uno por cada cuerpo que presenta al menos una instancia
            relacionada.
        """
        return get_recursos_asociados_por_cuerpo(self)

    def get_novedad(self):
        """
        Retorna la novedad que será mostrada en el pie de página.
        """
        return '{0!s}: {1!s}'.format(self.slug.title(), self.texto_pie_pagina)
