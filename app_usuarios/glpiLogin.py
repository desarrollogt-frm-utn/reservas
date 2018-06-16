from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from app_usuarios.models import Usuario
from app_parque_tecnologico.adapters.glpi_client.RESTClient import RESTClient
from reservas.settings.base import GLPI_URL

def obtener_pass_aleatoria():
    random = get_random_string().upper()
    return random

class GlpiLogin(object):

    def authenticate(self, username=None, password=None):
        glpi = RESTClient(GLPI_URL)

        try:
            user = glpi.connect(username, password)
        except Exception:
            user = None

        if user:
            perfil = glpi.getMyInfo()
            try:
                user = Usuario.objects.get(username=username)
            except Usuario.DoesNotExist:
                # Crea un nuevo usuario. La contraseña es seteada de
                # manera aleatoria debido a que la misma no sera utilizada;
                # Se comprueba el usuario con el metodo glpi.connect().
                try:
                    django_user = User.objects.get(username=username)
                    user = Usuario(user_ptr_id=django_user.pk)
                    user.__dict__.update(django_user.__dict__)
                except User.DoesNotExist:
                    user = Usuario(username=username, password=obtener_pass_aleatoria())
                    user.is_staff = False
                    user.is_superuser = False
                    user.first_name = perfil['firstname']
                    user.last_name = perfil['realname']
                    user.email = perfil['email']

                legajo = None
                if perfil['registration_number']:
                    try:
                        legajo = int(perfil['registration_number'])
                    except ValueError as e:
                        legajo = None
                    user.legajo = legajo
                if not legajo:
                    return None

                if perfil['phone']:
                    user.telefono = perfil['phone']
                if perfil['mobile']:
                    user.celular = perfil['mobile']
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None