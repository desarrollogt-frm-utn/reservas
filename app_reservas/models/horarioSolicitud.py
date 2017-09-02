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


TIPO_RECURSO = {
    '1': _(u'Aula'),
    '2': _(u'Laboratorio Informatico'),
    '3': _(u'Laboratorio'),
    '4': _(u'Recurso de ALI'),
}


class DiasSemanaField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DIAS_SEMANA.items()))
        kwargs['max_length'] = 1
        super(DiasSemanaField, self).__init__(*args, **kwargs)


class TipoRecursoField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(TIPO_RECURSO.items()))
        kwargs['max_length'] = 1
        super(TipoRecursoField, self).__init__(*args, **kwargs)

class HorarioSolicitud(models.Model):
    # Atributos

    dia = DiasSemanaField()

    fin = models.TimeField(
        verbose_name='Hora de Fin'
    )

    inicio = models.TimeField(
        verbose_name='Hora de Inicio'
    )

    tipoRecurso = TipoRecursoField()

    cantidad_alumnos = models.PositiveIntegerField(
        verbose_name='Cantidad de alumnos'
    )
    softwareRequerido = models.TextField(
        verbose_name='Software Requerido',
        null=True,
        blank=True,
    )

    # Relaciones

    solicitud = models.ForeignKey(
        'Solicitud',
        verbose_name='Solicitud',
    )

    tipoLaboratorio = models.ForeignKey(
        'TipoLaboratorio',
        verbose_name="Tipo de Laboratorio",
        null=True,
        blank=True,
    )
    tipoRecursoAli = models.ManyToManyField(
        'TipoRecursoAli',
        verbose_name='Tipo de Recurso ALI',
        blank=True,
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
