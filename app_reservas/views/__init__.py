from .ali import (
    AliTemplateView,
    AliVideoconferenciasDetailView,
)
from .area import AreaDetailView
from .aula import AulaDetailView
from .createViewSolicitud import SolicitudCreate
from .cuerpo import CuerpoDetailView
from .index import IndexView
from .laboratorio import LaboratorioDetailView
from .laboratorio_informatico import (
    LaboratorioInformaticoDetailView,
    LaboratorioInformaticoListView,
)
from .nivel import NivelDetailView
from .recurso import recurso_eventos_json
from .recurso_ali import RecursoAliDetailView
from .solicitud import (
    SolicitudAliReclamosSugerencias,
    SolicitudAulaView,
    SolicitudInstalacionSoftwareView,
    SolicitudLaboratorioInformaticoView,
    SolicitudMaterialMultimediaView,
)
from .tipo_laboratorio import TipoLaboratorioDetailView
from .tipo_recurso_ali import TipoRecursoAliDetailView
from .tv import (
    TvCuerposListView,
    TvVisorCuerposDetailView,
    TvVisorDetailView,
)
