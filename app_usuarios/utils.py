import base64
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


def validateEmail(email):
    """Método utilizado para validar emails"""
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def obtenerUsername(email):
    """obtiene el username a partir del email ingresado"""
    username = email.rsplit('@', 1)[0]
    UserModel = get_user_model()
    while UserModel.objects.filter(username=username).exists():
        username += get_random_string(2)
    return username
