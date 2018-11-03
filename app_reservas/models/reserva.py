import django
from django.db import models
from django.contrib.auth.models import User
from app_usuarios.models import Usuario
from app_academica.models import Comision, Docente


class Reserva(models.Model):
    # Atributos

    fecha_creacion = models.DateTimeField(
        verbose_name='Fecha de Creación',
        default=django.utils.timezone.now
    )

    fecha_inicio = models.DateField(
        verbose_name='Fecha de inicio de reserva'
    )

    fecha_fin = models.DateField(
        verbose_name='Fecha de fin de reserva',
        blank=True,
        null=True,
    )

    nombre_evento = models.CharField(
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

    docente = models.ForeignKey(
        Docente,
        verbose_name='Docente',
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
        return str(self.get_nombre_corto())

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = 'Reserva #{0!s} - {1!s}'.format(
            self.id,
            self.nombre_evento
        )
        return nombre_corto

    def get_estado_reserva(self):
        """
        Retorna el estado actual de la reserva
        """
        estado = self.historicoestadoreserva_set.filter(fecha_fin__isnull=True)[0]
        return estado
