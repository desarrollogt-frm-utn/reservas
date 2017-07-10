from django.db import models
from django.contrib.auth.models import User


class Reserva(models.Model):
    # Atributos

    fecha_creacion = models.DateTimeField(
        verbose_name='Fecha de Creación'
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

    horario = models.ForeignKey(
        'HorarioSolicitud',
        verbose_name='Horario de Solicitud',
        related_name='reservas'
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
        s = '{0!s} - {1!s} - {2!s}'.format(self.recurso, self.horario.solicitud.docente.nombre, self.fecha_creacion)
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = '{0!s} - {1!s}'.format(self.solicitud.docente.nombre, self.fecha_creacion)
        return nombre_corto
