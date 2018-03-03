from .glpi_client.RESTClient import RESTClient
from reservas.settings.base import GLPI_URL, GLPI_USER, GLPI_PASS


def get_data_glpi(id_incidente):
    glpi = RESTClient(GLPI_URL)
    json = []
    if glpi.connect(GLPI_USER, GLPI_PASS):
        incidente = glpi.getTicket(ticket=id_incidente)
        id_loc = incidente['locations_id']
        localizacion = "--"
        if id_loc != '0':
            loc = glpi.getObject(
                itemtype='location',
                id=id_loc,
            )
            localizacion = loc['completename']

        json.append(
            {
                'id': incidente['id'],
                'nombre': incidente['name'],
                'localizacion': localizacion,
            }
        )
        usuarios = []
        for usuario in incidente['users']['requester']:
            id_user = usuario['users_id']
            user = glpi.getObject(
                itemtype='user',
                id=id_user,
            )
            usuarios.append(
                {
                    'firstname': user['firstname'],
                    'lastname': user['realname'],
                }
            )
        json.append(usuarios)

    return json
