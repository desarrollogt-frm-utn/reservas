from django.contrib.auth.models import User
from .glpi_client.RESTClient import RESTClient
from reservas.settings.base import GLPI_URL


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
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Crea un nuevo usuario. La contraseña es seteada de
                # manera aleatoria debido a que la misma no sera utilizada;
                # Se comprueba el usuario con el metodo glpi.connect().
                user = User(username=username, password='GT2017!')
                user.is_staff = True
                user.is_superuser = False
                user.first_name = perfil['firstname']
                user.last_name = perfil['realname']
                user.email = perfil['email']
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None