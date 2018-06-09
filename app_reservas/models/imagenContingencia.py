# coding=utf-8

import os

from django.db import models


def establecer_destino_archivo_imagen(instance, filename):
    """
    Establece la ruta de destino para el archivo de imagen cargado a la instancia.
    """
    # Almacena el archivo en:
    # 'app_reservas/contingencia/<id_imagen>'
    ruta_archivos_ubicacion = 'app_reservas/contingencia/'
    filename = '{0!s}_{1!s}'.format(instance.id, filename)
    return os.path.join(ruta_archivos_ubicacion, filename)


class ImagenContingencia(models.Model):
    # Atributos

    imagen = models.ImageField(
        upload_to=establecer_destino_archivo_imagen,
        verbose_name='Imagen',
        help_text='Archivo de imagen.',
    )

    activo = models.BooleanField(
        default=False,
        verbose_name='Imagen Activa',
        help_text='Indica si la imagen de contingencia se encuentra activa. Solo puede haber una activa al mismo tiempo.',
    )
    descripcion = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción de la imagen',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['id']
        verbose_name = 'Imagen de contingencia'
        verbose_name_plural = 'Imágenes de contingencia'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return "Imagen {0!s} de contingencia".format(
            self.id,
        )

    def save(self, *args, **kwargs):
        if self.activo:
            # select all other active items
            qs = type(self).objects.filter(activo=True)
            # except self (if self already exists)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            # and deactive them
            qs.update(activo=False)

        super(ImagenContingencia, self).save(*args, **kwargs)

    def get_url(self):
        """
        Retorna la URL de la imagen.
        """
        return self.imagen.url
