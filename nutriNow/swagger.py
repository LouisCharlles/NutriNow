from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="NutriNow",
        default_version="v1",
        description="Uma API desenvolvida em Django feita para ser um serviço de marcar consultas com nutricionistas, gerar pdfs com planos alimentares dos pacientes, possuir um diário do paciente para calorias consumidas e atividades diárias(integração com inteligência artificial é uma opção em andamento). A aplicação permite cadastrar: pacientes e nutricionistas. Um paciente pode marcar consultas com nutricionistas e vizualizar as informações de suas consultas. O nutricionista pode vizualizar a consulta, agendar uma data e um horário para essa consulta, e definir se ela já foi realizada ou não. A aplicação também disponibilza as opções de atualizar as informações dos usuários e das consultas, assim como poder deleta-los se necessário.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@NutriNow.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)