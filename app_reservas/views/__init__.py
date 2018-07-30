from .ali import (
    AliTemplateView,
    AliVideoconferenciasDetailView,
    PrestamoElementAdd,
    PrestamoCreate,
    PrestamoConfirm,
    PrestamoDetail,
    PrestamoElementsRemove,
    PrestamoFinalize,
    PrestamoList,
    PrestamoRegister,

)
from .area import AreaDetailView
from .aula import AulaDetailView
from .cuerpo import CuerpoDetailView
from .fechasSemestre import FechasSemestreConfig
from .index import IndexView, LoginIndexView
from .laboratorio import LaboratorioDetailView
from .laboratorio_informatico import (
    LaboratorioInformaticoDetailView,
    LaboratorioInformaticoListView,
)
from .nivel import NivelDetailView
from .novedad import NovedadView
from .recurso import recurso_eventos_json
from .recurso_ali import RecursoAliDetailView
from .rolesManager import UserList, AsingRole, RemoveRole
from .recurso_sae import RecursoSAEDetailView
from .solicitud import (
    RecursoAssign,
    SolicitudAliReclamosSugerencias,
    SolicitudAulaView,
    SolicitudCreate,
    SolicitudInstalacionSoftwareView,
    SolicitudLaboratorioInformaticoView,
    SolicitudMaterialMultimediaView,
    SolicitudList,
    SolicitudDetail,
    SolicitudReject,
)
from .reserva import ReservaCreate, ReservaList, ReservaListDocente
from .tipo_laboratorio import TipoLaboratorioDetailView
from .tipo_recurso_ali import TipoRecursoAliDetailView
from .tipo_recurso_sae import TipoRecursoSAEDetailView

from .tv import (
    TvCuerposListView,
    TvVisorCuerposDetailView,
    TvVisorDetailView,
)
