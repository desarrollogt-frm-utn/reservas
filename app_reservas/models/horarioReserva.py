from django.db import models

from django.utils.translation import ugettext_lazy as _

DIAS_SEMANA = {
    '0': _(u'Lunes'),
    '1': _(u'Martes'),
    '2': _(u'Miércoles'),
    '3': _(u'Jueves'),
    '4': _(u'Viernes'),
    '5': _(u'Sábado'),
    '6': _(u'Domingo'),
}


class DiasSemanaField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DIAS_SEMANA.items()))
        kwargs['max_length'] = 1
        super(DiasSemanaField, self).__init__(*args, **kwargs)


class HorarioReserva(models.Model):
    # Atributos

    dia = DiasSemanaField()

    fin = models.TimeField(
        verbose_name='Hora de Fin'
    )

    inicio = models.TimeField(
        verbose_name='Hora de Inicio'
    )

    id_evento_calendar = models.CharField(
        max_length=255,
        verbose_name='Id del evento',
        blank=True,
        null=True
    )

    # Relaciones

    reserva = models.ForeignKey(
        'Reserva',
        verbose_name='Reserva',
        null=True,
        blank=True,
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Horario de la reserva'
        verbose_name_plural = 'Horarios de la reserva'

    def __str__(self):
        """
        Representación de la instancia.
        """
        s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.reserva
        return nombre_corto
