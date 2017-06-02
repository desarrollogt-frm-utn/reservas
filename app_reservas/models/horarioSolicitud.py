from django.db import models

from django.utils.translation import ugettext as _

DIAS_SEMANA = {
    '1': _(u'Lunes'),
    '2': _(u'Martes'),
    '3': _(u'Miércoles'),
    '4': _(u'Jueves'),
    '5': _(u'Viernes'),
    '6': _(u'Sábado'),
    '7': _(u'Domingo'),
}


class DiasSemanaField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DIAS_SEMANA.items()))
        kwargs['max_length'] = 1
        super(DiasSemanaField, self).__init__(*args, **kwargs)


class HorarioSolicitud(models.Model):
    # Atributos

    dia = DiasSemanaField()

    duracion = models.PositiveSmallIntegerField(
        verbose_name='Duración'
    )

    horaInicio = models.TimeField(
        verbose_name='Hora de Inicio'
    )

    # Relaciones

    solicitud = models.ForeignKey(
        'Solicitud',
        verbose_name='Horario de la solicitud',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Horario de la solicitud'
        verbose_name_plural = 'Horarios de la solicutud'


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
        nombre_corto = self.solicitud
        return nombre_corto