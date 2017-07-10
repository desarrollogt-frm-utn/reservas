import datetime
from constance import config
from django.utils import timezone


def obtener_siguiente_dia_vigente(dia, horario):
    now = timezone.now()
    # Comparo el día requerido con el día actual
    # Se resta uno para mantener compatibilidades entre datos del
    # servidor académico y los datos de weekday obtenidos por python
    if now.weekday() == dia-1:
        return datetime.datetime.combine(now.date(), horario).isoformat()
    elif now.weekday() < dia-1:
        dia = now.date() + datetime.timedelta(days=(dia-1)-now.weekday())
    else:
        dia = now.date() + datetime.timedelta(days=6-(now.weekday()-dia))
    return datetime.datetime.combine(dia, horario).isoformat()


def obtener_fecha_finalizacion_reserva(cuatrimestre):
    if cuatrimestre == '1':
        fecha_fin = config.FECHA_FIN_PRIMER_SEMESTRE
        if fecha_fin.year == timezone.now().year:
            return datetime.datetime.combine(fecha_fin, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")
        else:
            return timezone.datetime(timezone.now().year, 6, 25, 23, 00).strftime("%Y%m%dT%H%M%SZ")
    if cuatrimestre == '2' or cuatrimestre == '0':
        fecha_fin = config.FECHA_FIN_SEGUNDO_SEMESTRE
        if fecha_fin.year == timezone.now().year:
            return datetime.datetime.combine(fecha_fin, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")
        else:
            return timezone.datetime(timezone.now().year, 12, 19, 23, 00).strftime("%Y%m%dT%H%M%SZ")
