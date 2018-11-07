from django.db import models


class RecursoPrestamo(models.Model):

    # Relaciones

    recurso = models.ForeignKey(
        'BaseRecurso',
        verbose_name='Recurso',
        related_name='prestamos_all'
    )

    reserva = models.ForeignKey(
        'Reserva',
        verbose_name='Reserva',
        related_name='reservas_all'
    )

    prestamo = models.ForeignKey(
        'Prestamo',
        verbose_name='Prestamo',
        related_name='recursos_all'
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'RecursoPrestamo'
        verbose_name_plural = 'RecursoPrestamos'

    def __str__(self):
        """
        Representación de la instancia
        """
        s = 'RecursoPrestamo #{0!s}'.format(self.id)
        return s
