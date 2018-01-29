# coding=utf-8

from django.db import models

from .recurso import Recurso


def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


class RecursoAli(Recurso):
    # Atributos
    identificador = models.CharField(
        max_length=20,
        verbose_name='Identificador',
        help_text='Identificador del recurso. No debe incluirse el prefijo o sufijo propio del '
                  'tipo de recurso. Por ejemplo, si el identificador completo es "PM-078-DIE", en '
                  'este campo debe introducirse "078-DIE", ya que el prefijo "PM" es propio del '
                  'tipo de recurso "Proyector multimedia".',
    )
    # Relaciones
    tipo = models.ForeignKey(
        'TipoRecursoAli',
        verbose_name='Tipo',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['identificador']
        verbose_name = 'Recurso del ALI'
        verbose_name_plural = 'Recursos del ALI'

    @overrides(Recurso)
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
        if self.tipo.is_sufijo:
            return '{0!s}-{1!s}'.format(
                self.identificador,
                self.tipo.prefijo,
            )
        else:
            return '{0!s}-{1!s}'.format(
                self.tipo.prefijo,
                self.identificador,
            )

    def get_identificador_url(self):
        """
        Retorna el identificador utilizado para acceder a la URL de detalle de
        la instancia.
        """
        return self.identificador
