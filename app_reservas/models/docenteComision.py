from django.db import models


class DocenteComision(models.Model):
    # Atributos
    grado = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Grado',
    )

    #relaciones
    docente = models.ForeignKey(
        'Docente',
        verbose_name='Docente'
    )

    comision = models.ForeignKey(
        'Comision',
        verbose_name="Comisión",
        related_name='docenteComision'
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['grado']
        verbose_name = 'Docente de la comisión'
        verbose_name_plural = 'Docentes de la comisión'


    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.docente:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                      self.docente.get_nombre_corto())
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.grado
        return nombre_corto