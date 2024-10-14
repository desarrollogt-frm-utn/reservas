# coding=utf-8

from django.db import models


class TipoAula(models.Model):
    # Atributos
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre',
        help_text='Nombre del tipo de aula, en singular.',
    )
    nombre_plural = models.CharField(
        max_length=50,
        verbose_name='Nombre en plural',
        help_text='Nombre del tipo de aula, en plural.',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug',
        help_text='Etiqueta corta que identifica al tipo de aulas, y sólo puede contener '
                  'letras, números, guiones bajos y guiones medios. Generalmente es utilizada '
                  'para las direcciones URL. Por ejemplo, si el nombre del tipo de aula es '
                  '"Aulas Multimedia", un slug posible sería "aulas_multimedia" o '
                  '"multimedia".',
    )
    is_ali = models.BooleanField(
        default=False,
        verbose_name='Aula es arti',
        help_text='Indica si el tipo de aula es de tipo arti .',
    )
    
    is_visible_navbar = models.BooleanField(
        default=False,
        verbose_name='Visible en la navbar',
        help_text='Indica si el tipo de recurso se lista dentro de las opciones de Aulas, en la '
                  'navbar (barra de navegación superior) del sitio.',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        ordering = ['nombre']
        verbose_name = 'Tipo de Aula'
        verbose_name_plural = 'Tipos de Aula'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return self.nombre

    def get_aulas(self):
        """
        Retorna el listado de aulas asociadas a la instancia.
        """
        return self.aula_set.all()
