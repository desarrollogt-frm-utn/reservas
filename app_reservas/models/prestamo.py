from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Prestamo(models.Model):
    # Atributos
    inicio = models.DateTimeField(
        verbose_name='Inicio',
        default=timezone.now
    )

    fin = models.DateTimeField(
        verbose_name='Fin',
        blank=True,
        null=True,
    )

    # Relaciones

    asignado_por = models.ForeignKey(
        User,
        verbose_name='Asignado por',
        related_name='prestamos_asignados'
    )

    recibido_por = models.ForeignKey(
        User,
        verbose_name='Recibido por',
        related_name='prestamos_recibidos',
        blank=True,
        null=True,
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
