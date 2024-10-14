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

    tipo_recurso = TipoRecursoField()

    cantidad_alumnos = models.PositiveIntegerField(
        verbose_name='Cantidad de alumnos'
    )
    software_requerido = models.TextField(
        verbose_name='Software Requerido',
        null=True,
        blank=True,
    )

    # Relaciones

    solicitud = models.ForeignKey(
        'Solicitud',
        verbose_name='Solicitud',
    )

    tipo_laboratorio = models.ForeignKey(
        'TipoLaboratorio',
        verbose_name="Tipo de Laboratorio",
        null=True,
        blank=True,
    )
    tipo_aula = models.ForeignKey(
        'TipoAula',
        verbose_name='Tipo de aula',
        blank=True,
    )
    
    tipo_laboratorio = models.ForeignKey(
        'TipoLaboratorio',
        verbose_name="Tipo de Laboratorio",
       
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
