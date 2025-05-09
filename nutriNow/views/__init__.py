from .pacientes import (
    GetPacienteInfoView,
    UpdatePacienteView,
    DeletePacienteView,
    AdicionaAlimentoNoDiarioView,
)

from .nutricionistas import (
    GetNutricionistaInfoView,
    UpdateNutricionistaView,
    DeleteNutricionistaView,
    RetornaDiarioAlimentarDoPacienteView,
    AtualizaHorariosDisponiveis,
    ListarNutricionistasView,
)

from .consultas import (
    PacienteMarcaConsultaView,
    UsuarioVizualizaConsultaView,
    DefineConsultaComoRealizadaView,
    VizualizarListaDeConsultasView,
)

from .usuarios import (
    RegistroUsuarioView,
)

from .planos_alimentares import(
    CriarPlanoAlimentarView,
    GetPlanoAlimentarInfoView,
)

from.notificacoes import(
    MarcarNotificacaoComoLidaView,
)

from .token import(
    CustomTokenObtainPairAndIdView,
)
__all__ = [
    "GetPacienteInfoView",
    "UpdatePacienteView",
    "DeletePacienteView",
    "AdicionaAlimentoNoDiarioView",
    "GetNutricionistaInfoView",
    "UpdateNutricionistaView",
    "DeleteNutricionistaView",
    "PacienteMarcaConsultaView",
    "UsuarioVizualizaConsultaView",
    "DefineConsultaComoRealizadaView",
    "VizualizarListaDeConsultasView",
    "RegistroUsuarioView",
    "CriarPlanoAlimentarView",
    "GetPlanoAlimentarInfoView",
    "RetornaDiarioAlimentarDoPacienteView",
    "AtualizarHorariosDisponiveis",
    "ListarNutricionistasView",
    "MarcarNotificacaoComoLidaView",
    "CustomTokenObtainPairAndIdView",
]
