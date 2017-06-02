from django.db import models


class HistoricoEstadoSolicitud(models.Model):
    # Atributos
    fechaInicio = models.DateTimeField(
        verbose_name='Fecha de Inicio',
    )

    fechaFin = models.DateTimeField(
        verbose_name='Fecha de Fin',
        blank=True,
        null=True,
    )

    descripcionCierre = models.CharField(
        max_length=150,
        verbose_name='Descripción de cierre de solicitud'
    )


    #relaciones
    estadoSolicitud = models.ForeignKey(
        'EstadoSolicitud',
        verbose_name='Estado de la Solicitud',
    )

    solicitud= models.ForeignKey(
        'Solicitud',
        verbose_name='Solicitud',
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['fechaInicio']
        verbose_name = 'Historico del Estado de la Solicitud'
        verbose_name_plural = 'Historicos de los Estados de las Solicitudes'


    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.solicitud:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                      self.solicitud.get_nombre_corto())
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        s= '{0!s} - {1!s}'.format(self.estadoSolicitud.get_nombre_corto(),
                                  self.fechaInicio)
        return s