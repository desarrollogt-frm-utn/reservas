from django.db import models



class Materia(models.Model):
    # Atributos
    nombre = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nombre',
    )
    codigo = models.CharField(
        max_length=5,
        blank=False,
        verbose_name='Código',
    )

    #relaciones
    plan = models.ForeignKey(
        'Plan',
        verbose_name='Plan',
    )

    especialidad = models.ForeignKey(
        'Especialidad',
        verbose_name='Especialidad',
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['codigo']
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'


    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.nombre:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                      self.nombre)
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.codigo
        return nombre_corto