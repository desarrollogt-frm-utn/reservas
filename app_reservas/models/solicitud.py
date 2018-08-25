from django.db import models

from app_usuarios.models import Usuario as UsuarioModel
from app_academica.models import Docente, Comision

from django.utils.translation import ugettext_lazy as _

TIPO_SOLICITUD = {
    '1': _(u'Cursado Completo'),
    '2': _(u'Cursado - Un solo día'),
    '3': _(u'Fuera de Agenda - Periodo'),
    '4': _(u'Fuera de Agenda - Un solo día'),
}


class TipoSolicitudField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(TIPO_SOLICITUD.items()))
        kwargs['max_length'] = 1
        super(TipoSolicitudField, self).__init__(*args, **kwargs)


class Solicitud(models.Model):
    # Atributos
    fechaCreacion = models.DateTimeField(
        verbose_name='Fecha de Creación',
    )

    fechaInicio = models.DateField(
        verbose_name='Fecha de inicio de solicitud'
    )

    fechaFin = models.DateField(
        verbose_name='Fecha de fin de solicitud',
        blank=True,
        null=True,
    )

    tipoSolicitud = TipoSolicitudField()

    # relaciones

    docente = models.ForeignKey(
        Docente,
        verbose_name='Docente',
    )

    comision = models.ForeignKey(
        Comision,
        verbose_name='Comision',
        blank=True,
        null=True,
    )

    solicitante = models.ForeignKey(
        UsuarioModel,
        related_name='solicutudes',
        blank=True,
        null=True
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
            s = '{0!s} - {1!s} - {2!s}'.format(
                self.get_nombre_corto(),
                self.docente.get_nombre_corto(),
                self.comision.get_nombre_corto()
            )
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

    @property
    def get_estado_solicitud(obj):
        ultimo_historico_recurso = obj.historicoestadosolicitud_set.filter(
            fechaFin__isnull=True
        ).latest('fechaInicio')
        return ultimo_historico_recurso
