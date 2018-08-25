# coding=utf-8
from rolepermissions.roles import AbstractUserRole


#Roles
ADMINISTRADOR_ROLE = 'administrador'

# Permisos
ASSIGN_RECURSO_AULA = 'assign_recurso_aula'
ASSIGN_RECURSO_ALI = 'assign_recurso_ali'
ASSIGN_RECURSO_LABORATORIO = 'assign_recurso_laboratorio'
ASSIGN_RECURSO_LABORATORIO_INFORMATICO = 'assign_recurso_laboratorio_informatico'

CREATE_PRESTAMO = 'create_prestamo'
CREATE_RESERVA = 'create_reserva'


FINALIZE_PRESTAMO = 'finalize_prestamo'


class Soporte(AbstractUserRole):
    available_permissions = {
        ASSIGN_RECURSO_ALI: True,
        ASSIGN_RECURSO_LABORATORIO: True,
        ASSIGN_RECURSO_LABORATORIO_INFORMATICO: True,
        CREATE_RESERVA: True,
        FINALIZE_PRESTAMO: True
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
        CREATE_RESERVA: True,
        FINALIZE_PRESTAMO: True

    }


class Bedel(AbstractUserRole):
    available_permissions = {
        'edit_reserva_estado': True,
        ASSIGN_RECURSO_AULA: True,
        CREATE_RESERVA: True,
    }


class Aliano(AbstractUserRole):
    available_permissions = {
        'edit_reserva_estado': True,
        ASSIGN_RECURSO_ALI: True,
        ASSIGN_RECURSO_LABORATORIO_INFORMATICO: True,
        CREATE_RESERVA: True,
        FINALIZE_PRESTAMO: True
    }
