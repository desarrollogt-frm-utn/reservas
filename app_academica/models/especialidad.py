from django.db import models


class Especialidad(models.Model):
    # Atributos
    nombre = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Nombre',
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
    )
    codigo = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Codigo',
    )

    visible = models.BooleanField(
        default=False,
        verbose_name='Visible en administración de aulas'
    )


    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_academica'
        ordering = ['nombre']
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'


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
