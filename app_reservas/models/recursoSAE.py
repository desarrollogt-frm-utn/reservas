# coding=utf-8

from django.db import models

from .recurso import Recurso


class RecursoSAE(Recurso):
    # Atributos
    nombre = models.CharField(
        max_length=20,
        verbose_name='nombre',
        help_text='Nombre del recurso.',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug',
        help_text='Etiqueta corta que identifica al recurso, y sólo puede contener '
                  'letras, números, guiones bajos y guiones medios. Generalmente es utilizada '
                  'para las direcciones URL. Por ejemplo, si el nombre del tipo de recurso es '
                  '"Cancha 01", un slug posible sería "chancha_01" o '
                  '"cancha01".',
    )

    # Relaciones
    tipo = models.ForeignKey(
        'TipoRecursoSAE',
        verbose_name='Tipo',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['nombre']
        verbose_name = 'Recurso de la SAE'
        verbose_name_plural = 'Recursos de la SAE'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return '{0!s}: {1!s}'.format(
            self.tipo,
            self.get_nombre_corto(),
        )

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """

        return self.nombre

    def get_nombre_url(self):
        """
        Retorna el nombre utilizado para acceder a la URL de detalle de
        la instancia.
        """
        return self.slug
