# coding=utf-8

from django.db import models


class Novedad(models.Model):
    # Atributos
    texto_principal = models.TextField(
        verbose_name='Texto de la novedad',
        blank=True,
        null=True,
        help_text='Texto en formato html que será mostrado en las pantallas de novedades',
    )
    texto_pie_pagina = models.CharField(
        verbose_name='Texto del pie',
        blank=True,
        null=True,
        max_length=255,
        help_text='Texto que aparecerá en el pie de la página. Puede contener hasta 255 caracteres',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug',
        help_text='Etiqueta corta que identifica a la novedad carrusel, y sólo puede contener letras, '
                  'números, guiones bajos y guiones medios.'
    )
    # Relaciones
    carrusel = models.ForeignKey(
        'CarruselImagenes',
        related_name='novedades',
        verbose_name='Carrusel',
        blank=True,
        null=True,
        help_text='Carrusel de imagenes que será mostrado. En caso de ser nulo se mostrará el campo Texto Principal'
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return "Novedad {0!s}'".format(
            self.carrusel,
        )
