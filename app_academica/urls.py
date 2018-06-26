from django.conf.urls import url

from .serializer import get_materia_json, get_horarios_json, get_horarios, get_alumnos, get_comisiones_docentes, get_cursado, get_especialidades, get_materias

urlpatterns = [
    url(
        r'^api/materia/(?P<legajo>\d+)$',
        get_materia_json,
        name='materia_json'
    ),
    url(
        r'^api/data/horarios/$',
        get_horarios,
        name='horario_json'
    ),
    url(
        r'^api/data/especialidades/$',
        get_especialidades,
        name='especialidades_json'
    ),
    url(
        r'^api/data/materias/$',
        get_materias,
        name='materias_json'
    ),
    url(
        r'^api/data/alumnos/$',
        get_alumnos,
        name='alumnos_json'
    ),
    url(
        r'^api/data/comision/(?P<anio>\d+)/$',
        get_comisiones_docentes,
        name='comision_json'
    ),
    url(
        r'^api/data/cursado/(?P<anio>\d+)/(?P<legajo>\d+)/$',
        get_cursado,
        name='horario_json'
    ),
    url(
        r'^api/horarios/(?P<comision>\d+)$',
        get_horarios_json,
        name='comision_json'
    )
]
