# coding=utf-8

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from rolepermissions.roles import assign_role, remove_role
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.decorators import has_role_decorator


@has_role_decorator('administrador')
def UserList(request):
    search = request.GET.get('search', '')
    users_list = []
    if search:
        querys = (Q(username__icontains=search) | Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        users = User.objects.filter(querys).order_by('username')
    else:
        users = User.objects.all().order_by('username')
    for user in users:
        usr = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'tecnico': has_role(user, 'tecnico'),
            'soporte': has_role(user, 'soporte'),
            'administrador': has_role(user, 'administrador'),
            'bedel': has_role(user, 'bedel'),
            'aliano': has_role(user, 'aliano'),
        }
        users_list.append(usr)
    # Busco el recurso activo y le asgino el estado con el nombre "Activo"
    return render(request, 'app_reservas/user_roles_list.html', {'users': users_list})


@has_role_decorator('administrador')
def AsingRole(request, pk, role):
    user = User.objects.get(id=pk)
    assign_role(user, role)
    return redirect(reverse_lazy('user_roles'))


@has_role_decorator('administrador')
def RemoveRole(request, pk, role):
    user = User.objects.get(id=pk)
    remove_role(user, role)
    return redirect(reverse_lazy('user_roles'))
