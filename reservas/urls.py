# coding=utf-8

"""reservas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r'^' + settings.DJANGO_URL_PREFIX, include([
        url(
            r'^facturacion/',
            include('app_facturacion.urls')
        ),
        url(
            r'^admin/',
            include(admin.site.urls)
        ),
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT,
            }
        ),
        url(
            r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': settings.STATIC_ROOT,
            }
        ),
        url(
            r'',
            include('app_reservas.urls')
        ),
        url(
            r'^academico/',
            include('app_academica.urls')
        ),
        url(
            r'^cuentas/login/$',
            login,
            {'template_name':'app_reservas/login.html'},
            name='login'
        ),
        url(
            r'^logout/',
            logout_then_login,
            name='logout'
        ),
        url(
            r'^cuentas/',
            include('app_usuarios.urls')
        ),
        url(r'^captcha/', include('captcha.urls')),
        url(
            r'^parque_tecnologico/',
            include('app_parque_tecnologico.urls')
        ),
        ]
    )),
]
