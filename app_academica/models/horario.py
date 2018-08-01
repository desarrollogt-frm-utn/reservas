from django.db import models


DIAS_SEMANA = {
    '1': 'Lunes',
    '2': 'Martes',
    '3': 'Miércoles',
    '4': 'Jueves',
    '5': 'Viernes',
    '6': 'Sábado',
}


DIAS_SEMANA_LIST = [
    {
        'dia_nombre': 'Lunes',
        'dia': '1'
    },
    {
        'dia_nombre': 'Martes',
        'dia': '2'
    },
    {
        'dia_nombre': 'Miércoles',
        'dia': '3'
    },
    {
        'dia_nombre': 'Jueves',
        'dia': '4'
    },
    {
        'dia_nombre': 'Viernes',
        'dia': '5'
    },
    {
        'dia_nombre': 'Sábado',
        'dia': '6'
    }
]

class DiasSemanaField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DIAS_SEMANA.items()))
        kwargs['max_length'] = 1
        super(DiasSemanaField, self).__init__(*args, **kwargs)


class Horario(models.Model):
    # Atributos

    dia = DiasSemanaField()

    duracion = models.PositiveSmallIntegerField(
        verbose_name='Duración'
    )

    horaInicio = models.TimeField(
        verbose_name='Hora de Inicio'
    )

    # Relaciones

    comision = models.ForeignKey(
        'Comision',
        verbose_name='Horario',
    )

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_academica'
        verbose_name = 'Horario de cursado'
        verbose_name_plural = 'Horarios de cursado'


    def __str__(self):
        """
        Representación de la instancia.
        """
        if self.comision.materia:
            s = '{0!s} - {1!s}'.format(self.get_nombre_corto(),
                                      self.comision.materia.get_nombre_corto())
        else:
            s = '{0!s}'.format(self.get_nombre_corto())
        return s

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        nombre_corto = self.comision
        return nombre_corto