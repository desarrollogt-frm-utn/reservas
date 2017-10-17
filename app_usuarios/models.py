import os
from django.db import models

from django.contrib.auth.models import User

from django.core.validators import RegexValidator


def establecer_destino_archivo_imagen(instance, filename):
    """
    Establece la ruta de destino para el archivo de imagen cargado a la instancia.
    """
    # Almacena el archivo en:
    # 'app_reservas/carruseles/<carrusel>/<imagen>'
    ruta_archivos_ubicacion = 'app_usuarios/perfil/{}/'.format(
        instance.email.slug,
    )
    return os.path.join(ruta_archivos_ubicacion, filename)


class Docente(User):
    # Atributos

    legajo = models.PositiveIntegerField(
        blank=False,
        default=1,
    )

    telefono = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?[\d()*-]+$',
                message='El formato de número de teléfono es incorrecto.'
            )
        ],
        max_length=30,
        verbose_name='teléfono',
        blank=True,
        null=True
    )

    celular = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?[\d()*-]+$',
                message='El formato de número de teléfono es incorrecto.'
            )
        ],
        max_length=30,
        verbose_name='celular'
    )

    foto = models.ImageField(
        null=True,
        blank=True,
        upload_to=establecer_destino_archivo_imagen
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_usuarios'
        ordering = ['email']
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
        return self.username
