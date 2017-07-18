# coding=utf-8

from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.decorators import login_required

from .views import (
    CreateDocente,
    CreateDocenteConfirm
)


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
]
