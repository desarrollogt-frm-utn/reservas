from django.db import models



class AlumnoComision(models.Model):
    # Atributos
    legajo = models.PositiveIntegerField(
        verbose_name='Legajo',
    )

    #relaciones
    comision = models.ForeignKey(
        'Comision',
        verbose_name='Comision',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['legajo']
        verbose_name = 'Alumno de la comisión'
        verbose_name_plural = 'Alumnos de la Comisión'


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
        nombre_corto = self.legajo
        return nombre_corto