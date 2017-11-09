from django.db import models
from django.utils.translation import ugettext_lazy as _


ESTADO_SOLICITUD = {
    '1': _(u'Pendiente'),
    '2': _(u'En curso'),
    '3': _(u'Finalizada'),
    '4': _(u'Dada de baja por usuario'),
}


class EstadoSolicitudField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(ESTADO_SOLICITUD.items()))
        kwargs['max_length'] = 1
        super(EstadoSolicitudField, self).__init__(*args, **kwargs)


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

    # relaciones
    estadoSolicitud = EstadoSolicitudField()

    solicitud = models.ForeignKey(
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
            s = '{0!s} - {1!s}'.format(
                self.get_nombre_corto(),
                self.solicitud.get_nombre_corto()
                )
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        s = '{0!s} - {1!s}'.format(
            self.estadoSolicitud.get_nombre_corto(),
            self.fechaInicio
            )
        return s
