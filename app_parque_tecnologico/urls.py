# coding=utf-8

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import RecursoCreate, IncidenteView
from .serializers import get_nivel_json, get_tipo_componente_json, get_marcas_json, get_incidente_json, get_local_json


urlpatterns = [
    # url(
    #     r'^$',
    #     views.index,
    #     name='index'
    # ),
    url(
        r'^recurso/alta$',
        login_required(RecursoCreate.as_view()),
        name='recurso-alta'
    ),
    url(
        r'^api/nivel/$',
        get_nivel_json,
        name='nivel_json'
    ),
    url(
        r'^api/local/$',
        get_local_json,
        name='local_json'
    ),
    url(
        r'^api/tipo_componente/$',
        get_tipo_componente_json,
        name='tipo_componente_json'
    ),
    url(
        r'^api/marcas/$',
        get_marcas_json,
        name='marcas_json'
    ),
    url(
        r'^api/incidente/$',
        get_incidente_json,
        name='incidente_json'
    ),
    url(
        r'^incidente$',
        login_required(IncidenteView.as_view()),
        name='incidente'
    ),
]
