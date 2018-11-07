from django.db import models
from django.utils.crypto import get_random_string

from app_reservas.models.baseRecurso import BaseRecurso


def obtener_codigo_aleatorio():
    random = get_random_string().upper()
    while Accesorio.objects.filter(codigo=random).exists():
        random = get_random_string().upper()
    return random


class Accesorio(BaseRecurso):
    # Atributos
    identificador = models.CharField(
        max_length=255,
        verbose_name='Nombre',
    )

    # Relaciones
    tipo = models.ForeignKey(
        'TipoAccesorio',
        verbose_name='Tipo',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Accesorio'
        verbose_name_plural = 'Accesorios'

    def __str__(self):
        """
        Representación de la instancia
        """
        s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        if self.tipo:
            nombre_corto = "{0!s}: {1!s}".format(self.tipo, self.identificador)
        else:
            nombre_corto = self.identificador
        return nombre_corto

    def get_active_loan(self):
        prestamos = self.prestamos_all.filter(prestamo__fin=None)[:1]
        if prestamos:
            return prestamos[0]
        return None
