from django.db import models

from django.utils.translation import ugettext as _


CUATRIMESTRE = {
    '0': _(u'Anual'),
    '1': _(u'Primer Semestre'),
    '2': _(u'Segundo Semestre'),
}


class CuatrimestreField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(CUATRIMESTRE.items()))
        kwargs['max_length'] = 1
        super(CuatrimestreField, self).__init__(*args, **kwargs)


class Comision(models.Model):
    # Atributos
    comision = models.CharField(
        max_length=10,
        blank=False,
        verbose_name='Comisión',
    )

    anioacademico = models.PositiveSmallIntegerField(
        verbose_name='Año Académico'
    )

    codigo= models.PositiveIntegerField(
        verbose_name='Código de comisión',
        blank=True,
        null=True
    )

    cuatrimestre = CuatrimestreField()

    #relaciones
    materia = models.ForeignKey(
        'Materia',
        verbose_name='Materia',
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['comision']
        verbose_name = 'Comision'
        verbose_name_plural = 'Comisiones'


    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.materia:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                      self.materia.get_nombre_corto())
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.comision
        return nombre_corto

    def get_nombre_largo(self):
        """
        Reorna el nombre largo de la instancia.
        """
        if self.materia:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                      self.materia.nombre)
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s
