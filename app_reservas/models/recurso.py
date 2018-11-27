# coding=utf-8

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.crypto import get_random_string

from app_reservas.models.baseRecurso import BaseRecurso
from ..adapters.google_calendar import generar_lista_eventos
from app_reservas.utils import parse_eventos_response, get_now_timezone


def obtener_codigo_aleatorio():
    random = get_random_string().upper()
    while Recurso.objects.filter(codigo=random).exists():
        random = get_random_string().upper()
    return random


class Recurso(BaseRecurso):
    # Atributos
    calendar_codigo = models.CharField(
        max_length=100,
        verbose_name='ID del calendario',
        help_text='Puede conocerse al acceder a los detalles del calendario en Google Calendar. '
                  'Su formato habitual es: "identificador@group.calendar.google.com". '
                  'Por ejemplo, un valor válido es: '
                  '"pi4pfu4alasbojtd1v1bj32oc0@group.calendar.google.com".',
    )
    calendar_color = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Color del calendario',
        help_text='Color con el que se visualizan los eventos del calendario. '
                  'Debe estar en formato hexadecimal. Por ejemplo, un valor válido es: '
                  '"#ff8c0a"',
    )

    url_detalles = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name='URL de detalles',
        help_text='URL a la que se va a redirigir para obtener más info.'
                  'Puede ser nulo.',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return '{0!s}'.format(self.get_nombre_corto())

    # Método sobreescrito para el guardado de una instancia.
    def save(self, *args, **kwargs):
        # Guarda la instancia actual.
        super(Recurso, self).save(*args, **kwargs)
        # Encola la tarea de Celery para la obtención de los eventos de la instancia.
        from ..tasks import obtener_eventos_recurso_especifico
        obtener_eventos_recurso_especifico.delay(self)

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        return 'Recurso: {0:d}'.format(self.id)

    def get_eventos(self):
        return generar_lista_eventos(self.calendar_codigo)

    def get_eventos_json(self):
        eventos = self.get_eventos()

        eventos_json = parse_eventos_response(eventos, self.id)
        return eventos_json

    def get_nearby_reservations(self):
        from app_reservas.models import Reserva
        dia_reserva = get_now_timezone().weekday()
        reserva_qs = Reserva.objects.filter(
                 recurso__id=self.id,
                 historicoestadoreserva__estado='1',
                 historicoestadoreserva__fecha_fin__isnull=True,
                 horarioreserva__dia=dia_reserva
             )
        inicio = get_now_timezone() - timezone.timedelta(minutes=10)
        fin = get_now_timezone() + timezone.timedelta(minutes=100)
        neaby_reservation = []
        if settings.TEST:
            neaby_reservation = reserva_qs
        else:
            for reserva in reserva_qs:
                horario_obj = reserva.horarioreserva_set.get(dia=dia_reserva)
                if horario_obj.inicio > inicio.time() or horario_obj.inicio < fin.time():
                    neaby_reservation.append(reserva)
        return neaby_reservation

    def get_active_reservations(self, fecha_inicio = None, fecha_fin = None):
        from app_reservas.models import Reserva
        reservas_qs = Reserva.objects.filter(
            recurso__id=self.id,
            historicoestadoreserva__estado='1',
            historicoestadoreserva__fecha_fin__isnull=True
        )

        if fecha_inicio:
            reservas_qs = reservas_qs.filter(
                Q(semestre=0) | Q(semestre=semestre)
            )

        return reservas_qs
