# coding=utf-8

from django.template.defaultfilters import slugify

from ..models.aula import Aula
from ..models.laboratorio import Laboratorio
from ..models.laboratorioInformatico import LaboratorioInformatico
from ..models.recurso import Recurso


def get_recursos_asociados(instancia):
    """Retorna todos los recursos asociados a la instancia.

    Genera una lista conformada por diccionarios, uno por cada tipo de recurso asociado. Cada
    uno de estos diccionarios indica los nombres apropiados del tipo de recurso, y una lista
    con las instancias de ese tipo que están relacionadas a la instancia.
    En caso de que la instancia no tenga recursos relacionados de un cierto tipo, el
    diccionario de este tipo no es añadido a la lista.

    Parameters
    ----------
    instancia : object
        Instancia de la cual se obtienen sus recursos asociados.

    Returns
    -------
    list of dicts
        Lista de diccionarios, uno por cada tipo de recurso asociado que presenta al menos una
        instancia relacionada.
    """
    recursos = []
    tipos_recurso = [
        {
            'modelo': Aula,
            'slug': 'aula',
            'metodo': 'get_aulas',
        },
        {
            'modelo': Laboratorio,
            'slug': 'laboratorio',
            'metodo': 'get_laboratorios',
        },
        {
            'modelo': LaboratorioInformatico,
            'slug': 'laboratorio_informatico',
            'metodo': 'get_laboratorios_informatica',
        },
    ]

    # Itera entre los tipos de recursos especificados.
    for tipo in tipos_recurso:
        # Verifica que la instancia cuente con el método de obtención para el tipo actual.
        if hasattr(instancia, tipo['metodo']):
            # Obtiene los recursos asociados del tipo actual.
            elementos = getattr(instancia, tipo['metodo'])()
            # Verifica que se haya obtenido al menos un elemento asociado.
            if elementos:
                # Añade los recursos asociados del tipo actual.
                recursos.append(
                    {
                        'nombre_singular': tipo['modelo']._meta.verbose_name,
                        'nombre_plural': tipo['modelo']._meta.verbose_name_plural,
                        'slug': tipo['slug'],
                        'elementos': elementos,
                    }
                )

    return recursos


def get_recursos_asociados_por_cuerpo(instancia):
    """Retorna todos los recursos asociados a la instancia, separados por cuerpo.

    Genera una lista conformada por diccionarios, uno por cada cuerpo que presenta recursos
    asociados. Cada uno de estos diccionarios indica el cuerpo y una lista con las instancias de
    ese tipo que están relacionadas a la instancia.
    En caso de que la instancia no tenga recursos relacionados de un cuerpo, el diccionario de este
    cuerpo no es añadido a la lista.

    Parameters
    ----------
    instancia : object
        Instancia de la cual se obtienen sus recursos asociados.

    Returns
    -------
    list of dicts
        Lista de diccionarios, uno por cada cuerpo que presenta al menos una instancia relacionada.
    """
    lista_elementos = []

    # Obtiene los recursos asociados a la instancia.
    recursos = get_recursos_asociados(instancia)
    # Combina en una única lista todos los elementos de los diferentes tipos de recurso asociados.
    for tipo_recurso in recursos:
        lista_elementos.extend(tipo_recurso['elementos'])

    # Crea una lista con los cuerpos que presentan al menos un recurso relacionado (sin
    # repeticiones), y la ordena por el número de cuerpo.
    cuerpos = list({elemento.nivel.cuerpo for elemento in lista_elementos})
    cuerpos.sort(key=lambda cuerpo: cuerpo.numero)

    # Crea una lista con los recursos asociados a cada cuerpo.
    recursos_por_cuerpo = [
        {
            'cuerpo': cuerpo,
            'elementos': [
                elemento
                for elemento in lista_elementos
                if elemento.nivel.cuerpo == cuerpo
            ],
        } for cuerpo in cuerpos
    ]

    return recursos_por_cuerpo


def get_recurso_obj(id):
    recurso_obj = None
    try:
        recurso_obj = Recurso.objects.get(id=id)
    except Recurso.DoesNotExist:
        pass

    return recurso_obj
