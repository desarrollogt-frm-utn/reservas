from .ali import (
    AliTemplateView,
    AliVideoconferenciasDetailView,
)
from .area import AreaDetailView
from .aula import AulaDetailView
from .cuerpo import CuerpoDetailView
from .index import IndexView
from .laboratorio import LaboratorioDetailView
from .laboratorio_informatico import (
    LaboratorioInformaticoDetailView,
    LaboratorioInformaticoListView,
)
from .nivel import NivelDetailView
from .novedad import NovedadView
from .recurso import recurso_eventos_json
from .recurso_ali import RecursoAliDetailView
from .recurso_sae import RecursoSAEDetailView
from .solicitud import (
    SolicitudAliReclamosSugerencias,
    SolicitudAulaView,
    SolicitudInstalacionSoftwareView,
    SolicitudLaboratorioInformaticoView,
    SolicitudMaterialMultimediaView,
)
from .tipo_laboratorio import TipoLaboratorioDetailView
from .tipo_recurso_ali import TipoRecursoAliDetailView
from .tipo_recurso_sae import TipoRecursoSAEDetailView

from .tv import (
    TvCuerposListView,
    TvVisorCuerposDetailView,
    TvVisorDetailView,
)
