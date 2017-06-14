from django.db import models


class EstadoSolicitud(models.Model):
    # Atributos
    nombre = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nombre',
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['nombre']
        verbose_name = 'Estado de solicitud'
        verbose_name_plural = 'Estados de solicitudes'


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
        nombre_corto = self.nombre
        return nombre_corto