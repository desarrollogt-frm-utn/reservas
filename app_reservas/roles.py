# coding=utf-8
from rolepermissions.roles import AbstractUserRole


class Soporte(AbstractUserRole):
    available_permissions = {
        'edit_recurso_estado': True,
    }


class Tecnico(AbstractUserRole):
    available_permissions = {
        'edit_recurso_estado': True,
    }


class Administrador(AbstractUserRole):
    available_permissions = {
        'edit_recurso_estado': True,
    }


class Bedel(AbstractUserRole):
    available_permissions = {
        'edit_reserva_estado': True,
    }


class Aliano(AbstractUserRole):
    available_permissions = {
        'edit_reserva_estado': True,
    }
