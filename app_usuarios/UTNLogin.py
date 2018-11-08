import MySQLdb
import hashlib
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from app_usuarios.models import Usuario
from app_usuarios.utils import obtenerUsername
from django.conf import settings

def obtener_pass_aleatoria():
    random = get_random_string().upper()
    return random


class UTNLogin(object):
    def authenticate(self, username=None, password=None):
        try:
            db = MySQLdb.connect(host=settings.UTN_MYSQL_HOST, user=settings.UTN_MYSQL_USER, passwd=settings.UTN_MYSQL_PASS, db=settings.UTN_MYSQL_DB)
            cursor = db.cursor()
        except Exception:
            return None
        query = """
                    SELECT username, password2, name
                    FROM mailbox 
                    WHERE username='{0!s}';
                    """.format(username)

        try:
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            db.close()
        except Exception:
            row = None

        if row:
            m = hashlib.md5()
            m.update(password.encode('utf-8'))
            hashed_pass = m.hexdigest()
            if hashed_pass == row[1]:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    # Crea un nuevo usuario. La contraseña es seteada de
                    # manera aleatoria debido a que la misma no sera utilizada;
                    # Se comprueba el usuario con la clave del mail.
                    user = User(username=obtenerUsername(username), password=obtener_pass_aleatoria())
                    user.is_staff = False
                    user.is_superuser = False

                    if "," in row[2]:

                        first_name = row[2].split(",")[-1]
                        last_name = row[2].split(",")[0]
                    else:
                        first_name = row[2].split("  ")[0]
                        last_name = row[2].split("  ")[-1]
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = username
                    user.save()
                return user
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None
