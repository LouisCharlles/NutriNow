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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('novo_paciente/',views.CreatePacienteView.as_view(),name='novo_paciente'),
    path('novo_nutricionista/',views.CreateNutricionistaView.as_view(),name='novo_nutricionista'),
    path("info_paciente/<int:pk>/",views.GetPacienteInfoView.as_view(),name="info_paciente"),
    path("info_nutricionista/<int:pk>/",views.GetNutricionistaInfoView.as_view(),name="info_nutricionista"),
    path("atualizar_paciente/<int:pk>/",views.UpdatePacienteView.as_view(),name="atualizar_paciente"),
    path("atualizar_nutricionista/<int:pk>/",views.UpdateNutricionistaView.as_view(),name="atualizar_nutricionista"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
