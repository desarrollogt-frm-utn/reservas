# coding=utf-8

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.core.urlresolvers import reverse_lazy

from .views import (
    CreateDocente,
    CreateDocenteConfirm,
    DocenteApprove,
    DocenteDetail,
    DocenteReject,
    UserProfileDetail,
    UserProfileUpdate,
    UserProfileUpdateAdminView)


urlpatterns = [

    # Administración de usuarios
    url(
        r'^signup/$',
        CreateDocente,
        name='signup'
    ),
    url(
        r'^signup/(?P<code>[A-Za-z0-9=]+)$',
        CreateDocenteConfirm,
        name='signup-confirm'
    ),
    url(r'^reset/password_reset$',
        password_reset,
        {
            'template_name': 'app_usuarios/password_reset_form.html',
            'email_template_name': 'app_usuarios/email/password_reset.html'
        },
        name='password_reset'),
    url(r'^reset/password_reset_done$',
        password_reset_done,
        {'template_name': 'app_usuarios/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'app_usuarios/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done',
        password_reset_complete,
        {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete'),
    url(
        r'^usuario/(?P<pk>\d+)/$',
        login_required(DocenteDetail.as_view()),
        name='docente_detalle'),
    url(
        r'^usuario/aprobar/(?P<pk>\d+)/$',
        login_required(DocenteApprove),
        name='docente_approve'),
    url(
        r'^usuario/rechazar/(?P<pk>\d+)/$',
        login_required(DocenteReject),
        name='docente_reject'),

    url(
        r'^mi_perfil/$',
        login_required(UserProfileDetail.as_view()),
        name='my_profile'),
    url(
        r'^mi_perfil/editar$',
        login_required(UserProfileUpdate.as_view(success_url=reverse_lazy('my_profile'))),
        name='my_profile_edit'),

    url(
        r'^mi_perfil/editar$',
        login_required(UserProfileUpdate.as_view(success_url=reverse_lazy('my_profile'))),
        name='my_profile_edit'),

    url(
        r'^administracion_usuarios/editar/(?P<pk>\d+)$',
        login_required(UserProfileUpdateAdminView.as_view()),
        name='usuario_editar'
    ),
]
