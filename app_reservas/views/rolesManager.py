# coding=utf-8

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from app_usuarios.models import Docente
from app_usuarios.forms import FilterUsuariosForm

from rolepermissions.roles import assign_role, remove_role
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.decorators import has_role_decorator


@has_role_decorator('administrador')
def UserList(request):
    estado = FilterUsuariosForm()
    search = request.GET.get('search', '')
    filter_val = request.GET.get('estado', '')
    users_list = []
    if search:
        querys = (Q(username__icontains=search) | Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        users = User.objects.filter(querys).order_by('username')
    else:
        users = User.objects.all().order_by('username')
    # Filtro todos los usuarios que no poseen email
    users = users.exclude(email='None')
    if filter_val:
        if filter_val == '1':
            users = users.filter(is_active=True)
        elif filter_val == '2':
            users = users.filter(is_active=False)
    for user in users:
        docente_list = Docente.objects.filter(id=user.id)[:1]
        is_docente = False
        if docente_list:
            is_docente = True
        usr = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'tecnico': has_role(user, 'tecnico'),
            'soporte': has_role(user, 'soporte'),
            'administrador': has_role(user, 'administrador'),
            'bedel': has_role(user, 'bedel'),
            'aliano': has_role(user, 'aliano'),
            'is_docente': is_docente
        }
        users_list.append(usr)
    # Busco el recurso activo y le asgino el estado con el nombre "Activo"
    return render(request, 'app_reservas/user_roles_list.html', {'users': users_list, 'estado': estado})


@has_role_decorator('administrador')
def AsingRole(request, pk, role):
    user = User.objects.get(id=pk)
    assign_role(user, role)
    return redirect(request.META.get('HTTP_REFERER'))


@has_role_decorator('administrador')
def RemoveRole(request, pk, role):
    user = User.objects.get(id=pk)
    remove_role(user, role)
    return redirect(request.META.get('HTTP_REFERER'))
