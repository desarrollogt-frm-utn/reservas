# coding=utf-8
from rolepermissions.roles import AbstractUserRole


#Roles
ADMINISTRADOR_ROLE = 'administrador'

# Permisos
ASSIGN_RECURSO_AULA = 'assign_recurso_aula'
ASSIGN_RECURSO_ALI = 'assign_recurso_ali'
ASSIGN_RECURSO_LABORATORIO = 'assign_recurso_laboratorio'
ASSIGN_RECURSO_LABORATORIO_INFORMATICO = 'assign_recurso_laboratorio_informatico'


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
        'edit_docente_estado': True,
        ASSIGN_RECURSO_AULA: True,
        ASSIGN_RECURSO_ALI: True,
        ASSIGN_RECURSO_LABORATORIO: True,
        ASSIGN_RECURSO_LABORATORIO_INFORMATICO: True,

    }


class Bedel(AbstractUserRole):
    available_permissions = {
        'edit_reserva_estado': True,
        ASSIGN_RECURSO_AULA: True,
    }


class Aliano(AbstractUserRole):
    available_permissions = {
        'edit_reserva_estado': True,
        ASSIGN_RECURSO_ALI: True,
        ASSIGN_RECURSO_LABORATORIO_INFORMATICO: True,
    }
