from django.db import models
from django.utils.translation import ugettext_lazy as _


ESTADO_RESERVA = {
    '1': _(u'Activa'),
    '2': _(u'Finalizada'),
    '3': _(u'Dada de baja por usuario'),
    '4': _(u'Dada de baja por bedel'),
}

ESTADOS_FINALES = ['2', '3', '4']


class EstadoReservaField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(ESTADO_RESERVA.items()))
        kwargs['max_length'] = 1
        super(EstadoReservaField, self).__init__(*args, **kwargs)


class HistoricoEstadoReserva(models.Model):
    # Atributos
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha de Inicio',
    )

    fecha_fin = models.DateTimeField(
        verbose_name='Fecha de Fin',
        blank=True,
        null=True,
    )

    descripcion_cierre = models.CharField(
        max_length=150,
        verbose_name='Descripción de cierre de reserva'
    )

    # relaciones
    estado = EstadoReservaField()

    reserva = models.ForeignKey(
        'Reserva',
        verbose_name='Reservas',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['fecha_inicio']
        verbose_name = 'Historico del Estado de la Reserva'
        verbose_name_plural = 'Historicos de los Estados de las Reservas'

    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.reserva:
            s = '{0!s} - {1!s}'.format(
                self.get_nombre_corto(),
                self.reserva.get_nombre_corto())
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        s = '{0!s} - {1!s}'.format(
            self.estado,
            self.fecha_inicio)
        return s
