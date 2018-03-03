import json
from django.http import HttpResponse
from app_reservas.models import Nivel
from .models import TipoComponente, Marca, Local
from .adapters.glpi import get_data_glpi


def get_nivel_json(request):
    if request.is_ajax():
        cuerpo = request.GET.get('c')
        lista_niveles = []

        nivel_qs = Nivel.objects.filter(cuerpo=cuerpo)
        for n in nivel_qs:
            lista_niveles.append(
                {
                    'id': n.id,
                    'numero': n.numero,
                }
            )
        return HttpResponse(json.dumps(lista_niveles), content_type='application/json')


def get_local_json(request):
    if request.is_ajax():
        nivel = request.GET.get('n')
        lista_locales = []

        local_qs = Local.objects.filter(nivel=nivel)
        for l in local_qs:
            lista_locales.append(
                {
                    'id': l.id,
                    'numero': l.nro_local,
                }
            )
        return HttpResponse(json.dumps(lista_locales), content_type='application/json')


def get_tipo_componente_json(request):
    if request.is_ajax():
        lista_componentes = []
        tipo_componente_qs = TipoComponente.objects.all()
        for n in tipo_componente_qs:
            lista_componentes.append(
                {
                    'id': n.id,
                    'nombre': n.nombre,
                }
            )
        return HttpResponse(json.dumps(lista_componentes), content_type='application/json')


def get_marcas_json(request):
    if request.is_ajax():
        marcas = []
        marcas_qs = Marca.objects.all()
        for n in marcas_qs:
            marcas.append(
                {
                    'id': n.id,
                    'nombre': n.nombre,
                }
            )
        return HttpResponse(json.dumps(marcas), content_type='application/json')


def get_incidente_json(request):
    if request.is_ajax():
        id = request.GET.get('inc')
        incidente = get_data_glpi(id)

        return HttpResponse(json.dumps(incidente), content_type='application/json')
