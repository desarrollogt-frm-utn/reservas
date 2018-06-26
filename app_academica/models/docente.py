from django.db import models


class Docente(models.Model):
    # Atributos
    nombre = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Nombre',
    )
    correo = models.EmailField(
        max_length=255,
        blank=True,
        verbose_name='Correo',
    )
    legajo = models.PositiveIntegerField(
        blank=False,
        default=1,
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_academica'
        ordering = ['nombre']
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'


    def __str__(self):
        """
        Representación de la instancia
        """
        s = '{0!s}'.format(self.get_nombre_corto())
        return s


    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.nombre
        return nombre_corto
