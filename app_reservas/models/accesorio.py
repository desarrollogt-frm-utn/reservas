from django.db import models
from django.utils.crypto import get_random_string


def obtener_codigo_aleatorio():
    random = get_random_string().upper()
    while Accesorio.objects.filter(codigo=random).exists():
        random = get_random_string().upper()
    return random


class Accesorio(models.Model):
    # Atributos
    identificador = models.CharField(
        max_length=255,
        verbose_name='Nombre',
    )

    activo = models.BooleanField(default=True)

    codigo = models.CharField(
        max_length=12,
        unique=True,
        default=obtener_codigo_aleatorio
    )

    # Relaciones
    tipo = models.ForeignKey(
        'TipoAccesorio',
        verbose_name='Tipo',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Accesorio'
        verbose_name_plural = 'Accesorios'

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
        nombre_corto = self.identificador
        return nombre_corto

    def get_active_loan(self):
        prestamos = self.accesorios_all.filter(prestamo__fin=None)[:1]
        if prestamos:
            return prestamos[0]
        return None
