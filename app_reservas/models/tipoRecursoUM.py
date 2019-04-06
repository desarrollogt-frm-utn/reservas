# coding=utf-8

from django.db import models


class TipoRecursoUM(models.Model):
    # Atributos
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre',
        help_text='Nombre del tipo de recurso, en singular.',
    )
    nombre_plural = models.CharField(
        max_length=50,
        verbose_name='Nombre en plural',
        help_text='Nombre del tipo de recurso, en plural.',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug',
        help_text='Etiqueta corta que identifica al tipo de recurso, y sólo puede contener '
                  'letras, números, guiones bajos y guiones medios. Generalmente es utilizada '
                  'para las direcciones URL. Por ejemplo, si el nombre del tipo de recurso es '
                  '"Canchas de fútbol", un slug posible sería "canchas_futbol" o '
                  '"canchas".',
    )

    is_visible_navbar = models.BooleanField(
        default=False,
        verbose_name='Visible en la navbar',
        help_text='Indica si el tipo de recurso se lista dentro de las opciones de UM, en la '
                  'navbar (barra de navegación superior) del sitio.',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['nombre']
        verbose_name = 'Tipo de recurso de usos múltiple'
        verbose_name_plural = 'Tipos de recurso de usos múltiple'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return self.nombre