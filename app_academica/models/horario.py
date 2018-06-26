from django.db import models

from django.utils.translation import ugettext_lazy as _

DIAS_SEMANA = {
    '1': _(u'Lunes'),
    '2': _(u'Martes'),
    '3': _(u'Miercoles'),
    '4': _(u'Jueves'),
    '5': _(u'Viernes'),
    '6': _(u'Sabado'),
}


class DiasSemanaField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DIAS_SEMANA.items()))
        kwargs['max_length'] = 1
        super(DiasSemanaField, self).__init__(*args, **kwargs)


class Horario(models.Model):
    # Atributos

    dia = DiasSemanaField()

    duracion = models.PositiveSmallIntegerField(
        verbose_name='Duración'
    )

    horaInicio = models.TimeField(
        verbose_name='Hora de Inicio'
    )

    # Relaciones

    comision = models.ForeignKey(
        'Comision',
        verbose_name='Horario',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_academica'
        verbose_name = 'Horario de cursado'
        verbose_name_plural = 'Horarios de cursado'


    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.comision.materia:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                      self.comision.materia.get_nombre_corto())
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.comision
        return nombre_corto