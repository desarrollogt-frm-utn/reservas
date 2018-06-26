import django
from django.db import models
from django.contrib.auth.models import User
from app_usuarios.models import Usuario
from app_academica.models import Comision


class Reserva(models.Model):
    # Atributos

    fecha_creacion = models.DateTimeField(
        verbose_name='Fecha de Creación',
        default=django.utils.timezone.now
    )

    fechaInicio = models.DateField(
        verbose_name='Fecha de inicio de reserva'
    )

    fechaFin = models.DateField(
        verbose_name='Fecha de fin de reserva',
        blank=True,
        null=True,
    )

    nombreEvento = models.CharField(
        max_length=150,
        verbose_name='Nombre del evento',
    )

    # Relaciones

    asignado_por = models.ForeignKey(
        User,
        verbose_name='Asignado por'
    )

    recurso = models.ForeignKey(
        'Recurso',
        verbose_name='Recurso de la Reserva',
    )

    usuario = models.ForeignKey(
        Usuario,
        related_name='reservas',
        blank=True,
        null=True
    )

    comision = models.ForeignKey(
        Comision,
        verbose_name='Comision',
        blank=True,
        null=True,
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return str(self.id)

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        if self.docente:
            nombre_corto = '{0!s} - {1!s} {2!s} - {3!s}'.format(
                self.recurso,
                self.docente.first_name,
                self.docente.last_name,
                self.fecha_creacion
            )
        else:
            nombre_corto = '{0!s} - {1!s}'.format(
                self.recurso,
                self.fecha_creacion
            )
        return nombre_corto

    def get_estado_reserva(self):
        """
        Retorna el estado actual de la reserva
        """
        estado = self.historicoestadoreserva_set.filter(fechaFin__isnull=True)[0]
        return estado
