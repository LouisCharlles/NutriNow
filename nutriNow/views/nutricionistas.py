import json
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Nutricionista
from ..models import Paciente
from..models import Usuario
from ..serial import NutricionistaSerializer
from django.http import JsonResponse
from utils.user_permissions import IsNutricionista

class GetNutricionistaInfoView(APIView):
    """
    View para obter os dados de um nutricionista autenticado.
    Apenas o próprio nutricionista pode acessar suas informações.
    """

    permission_classes = [IsAuthenticated, IsNutricionista]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID do nutricionista a ser buscado",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                "Detalhes do nutricionista",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "nome": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "senha": openapi.Schema(type=openapi.TYPE_STRING),
                        "endereco": openapi.Schema(type=openapi.TYPE_STRING),
                        "telefone": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            404: "Nenhum nutricionista com este id foi encontrado.",
            400: "Erro na requisição.",
        },
    )
    def get(self,request,*args,**kwargs):
        """
        Retorna os detalhes de um nutricionista específico com base no id.

        Returns:
            JsonResponse: Informações do nutricionista se encontrado ou mensagem de erro caso contrário.
        """
        if request.user.is_nutricionista:
            try:
                nutricionista = Nutricionista.objects.get(pk=kwargs["pk"])
                serializer = NutricionistaSerializer(nutricionista)
                return Response(serializer.data, status=200)
            except Nutricionista.DoesNotExist:
                return Response({"error": "Nutricionista não encontrado."}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)      
        return JsonResponse({"Error":"Usuário não permitido realizar essa função."})


class UpdateNutricionistaView(APIView):
    """
    View responsável por atualizar as informações de um nutricionista existente.

    Métodos:
        patch(request): Atualiza os dados do nutricionista com base no token do nutricionista e os dados fornecidos na request.
    """

    permission_classes = [IsAuthenticated,IsNutricionista]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID do nutricionista a ser buscado",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "nome": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Nome do nutricionista"
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="E-mail do nutricionista"
                ),
                "senha": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Senha do nutricionista"
                ),
                "endereco": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Endereço do nutricionista"
                ),
                "telefone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Telefone do nutricionista"
                ),
                "horarios_disponiveis":openapi.Schema(
                    type=openapi.TYPE_OBJECT, description="Horários da semana disponíveis do nutricionista."
                )
            },
        ),
        responses={
            200: openapi.Response(
                description="Detalhes do nutricionista atualizado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "nome": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "senha": openapi.Schema(type=openapi.TYPE_STRING),
                        "telefone": openapi.Schema(type=openapi.TYPE_STRING),
                        "endereco": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            404: openapi.Response(
                description="Nenhum nutricionista foi encontrado.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Mensagem de erro"
                        )
                    },
                ),
            ),
            400: openapi.Response(
                description="Erro ao tentar atualizar o nutricionista.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Mensagem de erro"
                        )
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        if request.user.is_nutricionista:
            try:
                request_body = json.loads(request.body.decode("utf-8"))
                nutricionista_id = request_body["id_nutricionista"]
                nutricionista = Nutricionista.objects.get(pk=nutricionista_id)
                serializer = NutricionistaSerializer(
                    nutricionista, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=201, data=serializer.data)
            except Nutricionista.DoesNotExist:
                return JsonResponse({"error": "Nutricionista não encontrado."}, status=404)
            except Exception as e:
                return JsonResponse(status=400, data=f"Insira os dados corretamente. {e}")
        return JsonResponse({"Error":"Usuário não é nutricionista, não é permitido realizar essa funçao."})


class DeleteNutricionistaView(APIView):
    """
    View responsável por deletar um Nutricionista da base de dados.

    Métodos:
        delete(*args, **kwargs): Deleta o Nutricionista com base no ID fornecido.
    """

    permission_classes = [IsAuthenticated,IsNutricionista]
    manual_parameters = (
        [
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID do usuário a ser buscado",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
    )
    responses = {
        200: openapi.Response(
            description="Nutricionista deletado.",
        ),
        404: openapi.Response(
            description="Nenhum nutricionista com este ID foi encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Mensagem de erro"
                    )
                },
            ),
        ),
        400: openapi.Response(
            description="Erro ao tentar deletar o nutricionista.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Mensagem de erro"
                    )
                },
            ),
        ),
    }

    def delete(self,request):
        """
        Deleta um Nutricionista da base de dados com base no ID fornecido.

        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave contendo o ID do Nutricionista.

        Returns:
            JsonResponse: Confirmação de deleção ou mensagem de erro em caso de falha.
        """
        if request.user.is_nutricionista:
            try:
                request_body = json.loads(request.body.decode("utf-8"))
                nutricionista_id = request_body["id_nutricionista"]
                nutricionista = Nutricionista.objects.get(pk=nutricionista_id)
                nutricionista.delete()
                return JsonResponse(
                    "Nutricionista deletado com sucesso.", status=200, safe=False
                )
            except Nutricionista.DoesNotExist:
                return JsonResponse(
                    {
                        "status": "erro",
                        "mensagem": f"Nenhum nutricionista com este id foi encontrado.",
                    },
                    status=404,
                )
            except Exception as e:
                return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)
        return JsonResponse({"error":"Instância de usuário não é de nutricionista."})


class RetornaDiarioAlimentarDoPacienteView(APIView):
    permission_classes = [IsAuthenticated,IsNutricionista]

    def get(self,request,*args,**kwargs):
        usuario = request.user
        if usuario.is_nutricionista:
            try:
                paciente = Paciente.objects.get(pk=kwargs["pk"])
                return Response(
                    {"diario_alimentar": paciente.diario_alimentar},
                    status=status.HTTP_200_OK,
                )
            except Nutricionista.DoesNotExist:
                return Response(
                    {"error": "Nutricionista não encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Paciente.DoesNotExist:
                return Response(
                    {"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400, safe=False)
        return JsonResponse({"Error":"Usuário não é permitido ter acesso a essa função."})

class ListarNutricionistasView(APIView):
    """
    View responsável por listar todos os nutricionistas cadastrados.

    Métodos:
        get(request): Retorna uma lista de todos os nutricionistas cadastrados.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista todos os nutricionistas cadastrados.",
        responses={
            200: openapi.Response(
                description="Lista de nutricionistas retornada com sucesso.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="ID do nutricionista",
                            ),
                            "nome": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Nome do nutricionista",
                            ),
                            "email": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="E-mail do nutricionista",
                            ),
                            "telefone": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Telefone do nutricionista",
                            ),
                        },
                    ),
                ),
            ),
            401: openapi.Response(
                description="Não autorizado.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Mensagem de erro de autorização.",
                        )
                    },
                ),
            ),
        },
    )
    def get(self,*args, **kwargs):
        """
        Retorna uma lista de todos os nutricionistas cadastrados.

        Returns:
            Response: Lista de nutricionistas ou mensagem de erro.
        """
        try:
            nutricionistas = Nutricionista.objects.all()
            serializer = NutricionistaSerializer(nutricionistas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(
                {"error": f"Ocorreu um erro ao listar os nutricionistas: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class AtualizaHorariosDisponiveis(APIView):
    permission_classes = [IsAuthenticated,IsNutricionista]
    """
    View responsável por atualizar as informações dos horários disponíveis de um nutricionista.

    Métodos:
        patch(request): Atualiza os dados dos horários disponíveis com base no token do nutricionista e os dados fornecidos na request.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_nutricionista": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID do nutricionista"
                ),
                "horarios_disponiveis":openapi.Schema(
                    type=openapi.TYPE_OBJECT, description="Horários disponíveis de um nutricionista."
                )
            },
        ),
        responses={
            200: openapi.Response(
                description="Detalhes dos horários atualizados.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "horarios_disponiveis":openapi.Schema(type=openapi.TYPE_OBJECT)
                    },
                ),
            ),
            404: openapi.Response(
                description="Nenhum nutricionista foi encontrado.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Mensagem de erro"
                        )
                    },
                ),
            ),
            400: openapi.Response(
                description="Erro ao tentar atualizar os horários.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Mensagem de erro"
                        )
                    },
                ),
            ),
        },
    )
    def patch(self,request):
        usuario = request.user
        if not usuario.is_nutricionista:
            return JsonResponse({"erro":"Apenas nutricionistas podem acessar essa função."})
        try:
            nutricionista = Nutricionista.objects.get(usuario=usuario)
        except Nutricionista.DoesNotExist:
            return JsonResponse({"erro":"Nutricionista não encontrado"},status.HTTP_404_NOT_FOUND)
        
        serializer = NutricionistaSerializer(nutricionista,data=request.data,partial=True)
        horarios_disponiveis = request.data.get("horarios_disponiveis")
        if serializer.is_valid() and horarios_disponiveis:
            serializer.save()
            nutricionista.save()
            return JsonResponse(status=200, data=serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
