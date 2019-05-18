# coding=utf-8

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from app_reservas.views.reserva import ReservaFinalize, ReservaDetail, reserva_eventos_json, ReservaSincronizar
from .views import (
    AliTemplateView,
    AliVideoconferenciasDetailView,
    AsingRole,
    AulaDetailView,
    CuerpoDetailView,
    CustomAulaDetailView,
    FechasSemestreConfig,
    IndexView,
    LaboratorioDetailView,
    LaboratorioInformaticoDetailView,
    LaboratorioInformaticoListView,
    LoginIndexView,
    NivelDetailView,
    NovedadView,
    PrestamoCreate,
    PrestamoConfirm,
    PrestamoDetail,
    PrestamoElementAdd,
    PrestamoElementAddOnCreate,
    PrestamoElementsRemove,
    PrestamoFinalize,
    PrestamoList,
    PrestamoRegister,
    RecursoAssign,
    recurso_eventos_json,
    RecursoAliDetailView,
    reservaCreate,
    ReservaList,
    ReservaListDocente,
    RemoveRole,
    RecursoUMDetailView,
    SolicitudAliReclamosSugerencias,
    SolicitudAulaView,
    SolicitudCreate,
    SolicitudDetail,
    SolicitudInstalacionSoftwareView,
    SolicitudLaboratorioInformaticoView,
    SolicitudList,
    SolicitudMaterialMultimediaView,
    SolicitudReject,
    TipoLaboratorioDetailView,
    TipoRecursoAliDetailView,
    TipoRecursoUMDetailView,
    TvCuerposListView,
    TvVisorCuerposDetailView,
    TvVisorDetailView,
    UserList,
)

from .views.horarios import ComisionDetailView, HorariosComisionListView, horario_descargar

urlpatterns = [
    url(
        r'^$',
        IndexView.as_view(),
        name='index'
    ),
    url(
        r'^inicio/$',
        login_required(LoginIndexView.as_view()),
        name='login_index'
    ),
    url(
        r'^cuerpo/(?P<numero>\d+)/$',
        CuerpoDetailView.as_view(),
        name='cuerpo_detalle'
    ),
    url(
        r'^cuerpo/(?P<numero_cuerpo>\d+)/nivel/(?P<numero_nivel>-?\d+)/$',
        NivelDetailView.as_view(),
        name='nivel_detalle'
    ),
    url(
        r'^aula/(?P<pk>\d+)/$',
        AulaDetailView.as_view(),
        name='aula_detalle'
    ),
    url(
        r'^(?P<model>area|aulas)/(?P<slug>[-\w]+)/$',
        CustomAulaDetailView.as_view(),
        name='custom_aula_detalle'
    ),
    url(
        r'^recurso/(?P<pk>\d+)/eventos/$',
        recurso_eventos_json,
        name='recurso_eventos_json'
    ),
    url(
        r'^ali/$',
        AliTemplateView.as_view(),
        name='ali_index'
    ),
    url(
        r'^ali/videoconferencias/$',
        AliVideoconferenciasDetailView.as_view(),
        name='ali_videoconferencias_detalle'
    ),
    url(
        r'^laboratorios/informatica/$',
        LaboratorioInformaticoListView.as_view(),
        name='laboratorio_informatico_listado'
    ),
    url(
        r'^laboratorio/informatica/(?P<alias>[A-Za-z0-9]+)/$',
        LaboratorioInformaticoDetailView.as_view(),
        name='laboratorio_informatico_detalle'
    ),
    url(
        r'^laboratorios/(?P<slug>[-\w]+)/$',
        TipoLaboratorioDetailView.as_view(),
        name='tipo_laboratorio_detalle'
    ),
    url(
        r'^laboratorio/(?P<tipo>[A-Za-z0-9]+)/(?P<alias>[A-Za-z0-9]+)/$',
        LaboratorioDetailView.as_view(),
        name='laboratorio_detalle'
    ),
    url(
        r'^ali/(?P<slug>[-\w]+)/$',
        TipoRecursoAliDetailView.as_view(),
        name='tipo_recurso_ali_detalle'
    ),
    url(
        r'^ali/(?P<tipo>[-\w]+)/(?P<identificador>[A-Za-z0-9_-]+)/$',
        RecursoAliDetailView.as_view(),
        name='recurso_ali_detalle'
    ),
    url(
        r'^usos_multiple/(?P<slug>[-\w]+)/$',
        TipoRecursoUMDetailView.as_view(),
        name='tipo_recurso_um_detalle'
    ),
    url(
        r'^usos_multiple/(?P<tipo>[-\w]+)/(?P<slug>[A-Za-z0-9_-]+)/$',
        RecursoUMDetailView.as_view(),
        name='recurso_um_detalle'
    ),
    url(
        r'^solicitud/ali/reclamos_sugerencias/$',
        SolicitudAliReclamosSugerencias.as_view(),
        name='solicitud_ali_reclamos_sugerencias'
    ),
    url(
        r'^solicitud/aula/$',
        SolicitudAulaView.as_view(),
        name='solicitud_aula'
    ),
    url(
        r'^solicitud/instalacion_software/$',
        SolicitudInstalacionSoftwareView.as_view(),
        name='solicitud_instalacion_software'
    ),
    url(
        r'^solicitud/laboratorio/informatica/$',
        SolicitudLaboratorioInformaticoView.as_view(),
        name='solicitud_laboratorio_informatico'
    ),
    url(
        r'^solicitud/material_multimedia/$',
        SolicitudMaterialMultimediaView.as_view(),
        name='solicitud_material_multimedia'
    ),
    url(
        r'^tv/cuerpos/$',
        TvCuerposListView.as_view(),
        name='tv_cuerpos'
    ),
    url(
        r'^tv/visor/(?P<slug>[-\w]+)/$',
        TvVisorDetailView.as_view(),
        name='tv_visor'
    ),
    url(
        r'^tv/visor/(?P<slug>[-\w]+)/cuerpos/$',
        TvVisorCuerposDetailView.as_view(),
        name='tv_visor_cuerpos'
    ),

    url(
        r'^solicitud/nueva/$',
        login_required(SolicitudCreate),
        name='solicitud_nueva'
    ),

    url(
        r'^solicitudes/$',
        login_required(SolicitudList.as_view()),
        name='solicitud_listar'),
    url(
        r'^solicitud/(?P<pk>\d+)/$',
        login_required(SolicitudDetail.as_view()),
        name='solicitud_detalle'),
    url(
        r'^solicitud/baja/(?P<pk>\d+)/$',
        login_required(SolicitudReject),
        name='solicitud_baja'),

    url(
        r'^recurso/asignar/(?P<solicitud>\d+)/(?P<horario>\d+)$',
        login_required(RecursoAssign),
        name='recurso_assign'
    ),
    url(
        r'^mis_reservas/$',
        login_required(ReservaListDocente.as_view()),
        name='mis_reservas'),
    url(
        r'^reservas/crear/$',
        login_required(reservaCreate),
        name='reserva_crear'),
    url(
        r'^reservas/listar/$',
        login_required(ReservaList.as_view()),
        name='reserva_listar'),
    url(
        r'^reservas/finalizar/(?P<pk>\d+)/$',
        login_required(ReservaFinalize),
        name='reserva_finalizar'),
    url(
        r'^reservas/sincronizar/(?P<pk>\d+)/$',
        login_required(ReservaSincronizar),
        name='reserva_sincronizar'),

    url(
        r'^reservas/detalle/(?P<pk>\d+)/$',
        login_required(ReservaDetail.as_view()),
        name='reserva_detalle'),
    url(
        r'^reservas/(?P<pk>\d+)/eventos/$',
        login_required(reserva_eventos_json),
        name='reserva_eventos_json'
    ),
    url(
        r'^tv/novedad/(?P<slug>[-\w]+)/$',
        NovedadView.as_view(),
        name='tv_visor'
    ),
    # TODO: Eliminar. Vistas obsoletas debido a las vistas de VisorTv. Sólo se
    # mantienen para compatibilidad con los visores que funcionan actualmente.
    url(
        r'^tv/bedelia/(?P<slug>[-\w]+)/$',
        TvVisorDetailView.as_view(),
        name='tv_bedelia'
    ),
    url(
        r'^tv/bedelia/(?P<slug>[-\w]+)/cuerpos/$',
        TvVisorCuerposDetailView.as_view(),
        name='tv_bedelia_cuerpos'
    ),


    # Ali Prestamos
    url(
        r'^prestamos/registrar/$',
        login_required(PrestamoRegister),
        name='prestamo_registar'),

    url(
        r'^prestamos/crear/$',
        login_required(PrestamoCreate),
        name='prestamo_crear'),

    url(
        r'^prestamos/detalle/(?P<pk>\d+)$',
        login_required(PrestamoDetail.as_view()),
        name='prestamo_detalle'),

    url(
        r'^prestamos/finalizar/(?P<pk>\d+)/$',
        login_required(PrestamoFinalize),
        name='prestamo_finalizar'),
    url(
        r'^prestamos/listar/$',
        login_required(PrestamoList.as_view()),
        name='prestamo_listar'),
    url(
        r'^prestamos/agregar_elemento/$',
        login_required(PrestamoElementAddOnCreate),
        name='prestamo_creacion_agregar_elemento'
    ),
    url(
        r'^prestamos/agregar_elemento/(?P<pk>\d+)$',
        login_required(PrestamoElementAdd),
        name='prestamo_agregar_elemento'
    ),
    url(
        r'^prestamos/quitar_elementos/$',
        login_required(PrestamoElementsRemove),
        name='prestamo_quitar_elementos'),
    url(
        r'^prestamos/confirmar/$',
        login_required(PrestamoConfirm),
        name='prestamo_confirmar'),

    # Administración de usuarios
    url(
        r'^administracion_usuarios/$',
        login_required(UserList),
        name='user_roles'
    ),
    url(
        r'^administracion_fechas_semestre/$',
        login_required(FechasSemestreConfig),
        name='fechas_semestre_config'
    ),
    url(
        r'^administracion_usuarios/asignar/(?P<role>[A-Za-z]+)/(?P<pk>\d+)$',
        login_required(AsingRole),
        name='user_asing_role'
    ),
    url(
        r'^administracion_usuarios/quitar/(?P<role>[A-Za-z]+)/(?P<pk>\d+)$',
        login_required(RemoveRole),
        name='user_remove_role'
    ),

    url(r'^administracion_aulas/horario_comisiones/$',
        HorariosComisionListView.as_view(),
        name='comisiones_listar'
    ),

    url(r'^administracion_aulas/horario_comisiones/descargar$',
        login_required(horario_descargar),
        name='comisiones_horarios_descargar'
    ),

url(r'^administracion_aulas/horario_comisiones/comision/(?P<pk>\d+)$',
        ComisionDetailView.as_view(),
        name='comision_detalle'
    ),
]
