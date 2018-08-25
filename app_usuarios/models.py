import os
from django.db import models

from django.contrib.auth.models import User

from app_reservas.models import Area

from django.core.validators import RegexValidator
from django.utils.text import slugify


def establecer_destino_archivo_imagen(instance, filename):
    """
    Establece la ruta de destino para el archivo de imagen cargado a la instancia.
    """
    # Almacena el archivo en:
    # 'app_reservas/carruseles/<carrusel>/<imagen>'
    ruta_archivos_ubicacion = 'app_usuarios/perfil/{}/'.format(
        slugify(instance.username),
    )
    nombre_imagen = filename.split('.')[0] if '.' in filename else filename
    extension_imagen = filename.split('.')[-1] if '.' in filename else ''
    nombre_imagen = '%s.%s' % (slugify(str(nombre_imagen)), extension_imagen)
    return os.path.join(ruta_archivos_ubicacion, nombre_imagen)


class Usuario(User):
    # Atributos

    legajo = models.PositiveIntegerField(
        blank=False,
        unique=True,
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
        verbose_name='celular',
        blank=True,
        null=True
    )

    foto = models.ImageField(
        null=True,
        blank=True,
        upload_to=establecer_destino_archivo_imagen
    )

    areas = models.ManyToManyField(
        Area,
        blank=True,
        verbose_name='Áreas',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_usuarios'
        ordering = ['email']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


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
