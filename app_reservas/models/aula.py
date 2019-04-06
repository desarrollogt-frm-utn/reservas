# coding=utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify

from .recurso import Recurso


def establecer_destino_archivo_ubicacion(instance, filename):
    """
    Establece la ruta de destino para el archivo de ubicación cargado a la instancia.
    """
    # Almacena el archivo en: 'app_reservas/ubicaciones/aulas/<nombre_completo>.<extension>'
    ruta_archivos_ubicacion = 'app_reservas/ubicaciones/aulas/'
    extension_archivo = filename.split('.')[-1] if '.' in filename else ''
    nombre_archivo = '{0!s}.{1!s}'.format(slugify(str(instance)), extension_archivo)
    return os.path.join(ruta_archivos_ubicacion, nombre_archivo)


class Aula(Recurso):
    # Atributos
    numero = models.PositiveSmallIntegerField(
        verbose_name='Número',
        help_text='Número del aula. En caso de que no corresponda, introducir "0".',
    )
    nombre = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nombre',
        help_text='Nombre del aula, en caso de que posea. En caso de que no corresponda, dejar el '
                  'campo vacío. Por ejemplo, "Aula de dibujo".',
    )
    capacidad = models.PositiveSmallIntegerField(
        verbose_name='Capacidad',
        help_text='Capacidad del aula. En caso de que no corresponda, introducir "0".',
    )
    archivo_ubicacion = models.FileField(
        upload_to=establecer_destino_archivo_ubicacion,
        blank=True,
        verbose_name='Archivo de ubicación',
        help_text='Archivo que indica la ubicación del aula dentro de la facultad.',
    )
    # Relaciones
    areas = models.ManyToManyField(
        'Area',
        verbose_name='Áreas a cargo',
    )
    nivel = models.ForeignKey(
        'Nivel',
        verbose_name='Nivel',
    )

    tipo =models.ManyToManyField(
        'TipoAula',
        verbose_name='Tipo de Aula'
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['nivel', 'numero', 'nombre']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        """
        Representación de la instancia.
        """
        nombre = '{0!s} - {1!s}'.format(self.get_nombre_corto(), self.nivel)
        if self.capacidad:
            nombre += ' - Capacidad: {0!s}'.format(self.capacidad)
        return nombre

    def get_aula_nivel(self):
        """
        Retorna el nombre la instancia junto al nivel.
        """
        return '{0!s} - {1!s}'.format(self.get_nombre_corto(), self.nivel)

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.nombre or 'Aula {0:d}'.format(self.numero)
        return nombre_corto

    def get_identificador_url(self):
        """
        Retorna el identificador utilizado para acceder a la URL de detalle de
        la instancia.
        """
        return str(self.id)
