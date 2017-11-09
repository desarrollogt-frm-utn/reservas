from django.db import models

from django.contrib.auth.models import User


class Prestamo(models.Model):
    # Atributos
    inicio = models.DateTimeField(
        verbose_name='Fecha de Inicio',
    )

    fin = models.DateTimeField(
        verbose_name='Fecha de Fin',
        blank=True,
        null=True,
    )

    # Relaciones

    asignado_por = models.ForeignKey(
        User,
        verbose_name='Asignado por'
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Prestamo'
        verbose_name_plural = 'Prestamos'

    def __str__(self):
        """
        Representación de la instancia
        """
        s = 'Prestamo #{0!s}'.format(self.id)
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.id
        return nombre_corto
