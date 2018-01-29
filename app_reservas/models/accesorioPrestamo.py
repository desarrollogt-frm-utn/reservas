from django.db import models


class AccesorioPrestamo(models.Model):

    # Relaciones

    accesorio = models.ForeignKey(
        'Accesorio',
        verbose_name='Accesorio',
        related_name='accesorios_all'
    )

    prestamo = models.ForeignKey(
        'Prestamo',
        verbose_name='Prestamo',
        related_name='prestamosAccesorios_all'
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'AccesorioPrestamo'
        verbose_name_plural = 'AccesorioPrestamos'

    def __str__(self):
        """
        Representación de la instancia
        """
        s = 'AccesorioPrestamo #{0!s}'.format(self.id)
        return s
