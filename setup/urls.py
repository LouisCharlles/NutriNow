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
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
urlpatterns = [
    path('admin/', admin.site.urls),
    path("info_paciente/<int:pk>/",views.GetPacienteInfoView.as_view(),name="info_paciente"),
    path("info_nutricionista/<int:pk>/",views.GetNutricionistaInfoView.as_view(),name="info_nutricionista"),
    path("atualizar_paciente/<int:pk>/",views.UpdatePacienteView.as_view(),name="atualizar_paciente"),
    path("atualizar_nutricionista/<int:pk>/",views.UpdateNutricionistaView.as_view(),name="atualizar_nutricionista"),
    path("deletar_paciente/<int:pk>/",views.DeletePacienteView.as_view(),name="deletar_paciente"),
    path("deletar_nutricionista/<int:pk>/",views.DeleteNutricionistaView.as_view(),name="deletar_nutricionista"),
    path('criar_consulta/',views.PacienteMarcaConsultaView.as_view(),name="criar_consulta"),
    path('retorna_consulta/<int:pk>/',views.UsuarioVizualizaConsultaView.as_view(),name="retorna_consulta"),
    path('realizar_consulta/<int:pk>/',views.DefineConsultaComoRealizadaView.as_view(),name="realizar_consulta"),
    path('lista_consultas/<int:pk>/',views.VizualizarListaDeConsultasView.as_view(),name="lista_consultas"),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('registrar_usuario/', views.RegistroUsuarioView.as_view(), name='registrar_usuario'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
