from django.db import models

from django.utils.translation import ugettext as _

TIPO_RECURSO = {
    '1': _(u'Aula'),
    '2': _(u'Laboratorio Informatico'),
    '3': _(u'Laboratorio'),
    '4': _(u'Recurso de ALI'),
}

class TipoRecursoField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(TIPO_RECURSO.items()))
        kwargs['max_length'] = 1
        super(TipoRecursoField, self).__init__(*args, **kwargs)

class Solicitud(models.Model):
    # Atributos
    fechaCreacion = models.DateTimeField(
        verbose_name='Fecha de Creación',
    )

    horaInicio = models.TimeField(
        verbose_name='Hora de Inicio'
    )

    horaFin = models.TimeField(
        verbose_name='Hora de Fin'
    )

    tipoRecurso = TipoRecursoField()

    # relaciones
    tipoSolicitud = models.ForeignKey(
        'TipoSolicitud',
        verbose_name='Tipo de la Solicitud',
    )

    docente= models.ForeignKey(
        'Docente',
        verbose_name='Docente',
    )

    comision = models.ForeignKey(
        'Comision',
        verbose_name='Comision',
        blank=True,
        null=True,
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['fechaCreacion']
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'


    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.comision:
            s = '{0!s} - {1!s} - {2!s}'.format(self.get_nombre_corto(),
                                      self.docente.get_nombre_corto(),
                                               self.comision.get_nombre_corto())
        else:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                       self.docente.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.fechaCreacion
        return nombre_corto