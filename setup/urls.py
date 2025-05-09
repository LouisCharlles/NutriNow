"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from nutriNow import views
from rest_framework_simplejwt.views import TokenRefreshView 
from nutriNow.swagger import schema_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path("info_paciente/<int:pk>/",views.GetPacienteInfoView.as_view(),name="info_paciente"),
    path("info_nutricionista/<int:pk>/",views.GetNutricionistaInfoView.as_view(),name="info_nutricionista"),
    path("atualizar_paciente/",views.UpdatePacienteView.as_view(),name="atualizar_paciente"),
    path("atualizar_nutricionista/",views.UpdateNutricionistaView.as_view(),name="atualizar_nutricionista"),
    path("deletar_paciente/",views.DeletePacienteView.as_view(),name="deletar_paciente"),
    path("deletar_nutricionista/",views.DeleteNutricionistaView.as_view(),name="deletar_nutricionista"),
    path('criar_consulta/',views.PacienteMarcaConsultaView.as_view(),name="criar_consulta"),
    path('retorna_consulta/<int:pk>/',views.UsuarioVizualizaConsultaView.as_view(),name="retorna_consulta"),
    path('realizar_consulta/',views.DefineConsultaComoRealizadaView.as_view(),name="realizar_consulta"),
    path('lista_consultas/<int:pk>/',views.VizualizarListaDeConsultasView.as_view(),name="lista_consultas"),
    path('api/token/',views.CustomTokenObtainPairAndIdView.as_view(),name='token_obtain_pair_and_id'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('registrar_usuario/', views.RegistroUsuarioView.as_view(), name='registrar_usuario'),
    path('criar_plano_alimentar/',views.CriarPlanoAlimentarView.as_view(),name="criar_plano"),
    path("retorna_plano_alimentar/<int:pk>/",views.GetPlanoAlimentarInfoView.as_view(),name="retorna_plano_alimentar"),
    path('adicionar_alimento_no_diario/',views.AdicionaAlimentoNoDiarioView.as_view(),name="adicionar_alimento_no_diario"),
    path('retornar_diario_alimentar/<int:pk>/',views.RetornaDiarioAlimentarDoPacienteView.as_view(),name="retornar_diario_alimentar"),
    path('atualiza_horarios_disponiveis/',views.AtualizaHorariosDisponiveis.as_view(),name='atualiza_horarios_disponiveis'),
    path('listar_nutricionistas/', views.ListarNutricionistasView.as_view(), name='listar_nutricionistas'),
    path('ler_notificacao/<int:pk>/',views.MarcarNotificacaoComoLidaView.as_view(),name="ler_notificacao"),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
