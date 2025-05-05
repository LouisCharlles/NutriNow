from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Notificacao

class MarcarNotificacaoComoLidaView(APIView):
    """
    View responsável por marcar uma notificação como lida.

    Métodos:
    - patch(request, pk): Atualiza o status da notificação para lida, com base no ID fornecido.

    Permissões:
    - Requer autenticação (token JWT ou sessão autenticada).
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Marcar notificação como lida",
        operation_description="Atualiza o status de uma notificação para lida com base no ID da notificação.",
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID da notificação a ser marcada como lida",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Notificação marcada como lida com sucesso.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "Mensagem": openapi.Schema(type=openapi.TYPE_STRING, example="Notificação lida com sucesso.")
                    }
                )
            ),
            404: openapi.Response(
                description="Notificação não encontrada.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "erro": openapi.Schema(type=openapi.TYPE_STRING, example="Notificação não encontrada.")
                    }
                )
            )
        }
    )

    def patch(self,request,pk):
        """
        Atualiza o status da notificação para lida com base no ID.

        Parâmetros:
        - request (HttpRequest): Requisição HTTP.
        - pk (int): ID da notificação a ser atualizada.

        Retorna:
        - Response: Mensagem de sucesso ou erro caso a notificação não seja encontrada.
        """
        try:
            notificacao = Notificacao.objects.get(pk=pk)
            notificacao.lida = True
            notificacao.save()
            return Response({"Mensagem":"Notificação lida com sucesso."})
        except Notificacao.DoesNotExist:
            return Response({"erro": "Notificação não encontrada."}, status=404)