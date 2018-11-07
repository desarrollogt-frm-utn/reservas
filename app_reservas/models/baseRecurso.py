from django.db import models
from django.utils.crypto import get_random_string


def obtener_codigo_aleatorio():
    random = get_random_string().upper()
    while BaseRecurso.objects.filter(codigo=random).exists():
        random = get_random_string().upper()
    return random


class BaseRecurso(models.Model):
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    activo = models.BooleanField(default=True)

    codigo = models.CharField(
        max_length=12,
        unique=True,
        default=obtener_codigo_aleatorio
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Base del Recurso'
        verbose_name_plural = 'Bases de los Recursos'

    def __str__(self):
        """
        Representación de la instancia
        """

        return "Recurso #{0!s}".format(self.pk)
