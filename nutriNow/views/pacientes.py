import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Paciente
from ..serial import PacienteSerializer
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from utils.user_permissions import IsPaciente
class GetPacienteInfoView(APIView):
    """
    View para buscar as informações de um paciente pelo seu ID.
    
    Métodos:
        get(*args, **kwargs): Retorna os detalhes do paciente baseado no id.
    """
    permission_classes = [IsAuthenticated,IsPaciente]
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do usuário a ser buscado",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200:openapi.Response('Detalhes do paciente',openapi.Schema(type=openapi.TYPE_OBJECT,properties={
            'id':openapi.Schema(type=openapi.TYPE_INTEGER),
            'nome':openapi.Schema(type=openapi.TYPE_STRING),
            'email':openapi.Schema(type=openapi.TYPE_STRING),
            "senha":openapi.Schema(type=openapi.TYPE_STRING),
            'idade':openapi.Schema(type=openapi.TYPE_INTEGER),
            'peso':openapi.Schema(type=openapi.TYPE_NUMBER),
            'altura':openapi.Schema(type=openapi.TYPE_NUMBER),
            'genero':openapi.Schema(type=openapi.TYPE_STRING),
            'endereco':openapi.Schema(type=openapi.TYPE_STRING),
            'telefone':openapi.Schema(type=openapi.TYPE_STRING),
            'data_nascimento':openapi.Schema(type=openapi.TYPE_STRING,format=openapi.FORMAT_DATETIME),
        })),
        404:'Nenhum paciente com este id foi encontrado.',
        400: 'Erro na requisição.'
    })
    def get(self,request,*args,**kwargs):
        """
        Retorna os detalhes de um paciente específico com base no Token.
        
        Returns:
            JsonResponse: Informações do paciente se encontrado ou mensagem de erro caso contrário.
        """
        if request.user.is_paciente:
            try:
                paciente_id = kwargs["pk"]
                paciente = Paciente.objects.get(pk=paciente_id)
                serializer = PacienteSerializer(paciente)
                return Response(serializer.data, status=200)
            except Paciente.DoesNotExist:
                return Response({"error": "Paciente não encontrado."}, status=404)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return JsonResponse({"Error":"Usuário não é paciente, função não é permitida."})
        
class UpdatePacienteView(APIView):
    """
    View responsável por atualizar as informações de um paciente existente.
    
    Métodos:
        patch(request): Atualiza os dados do paciente com base no token fornecido e os dados na request.
    """
    permission_classes = [IsAuthenticated,IsPaciente]
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do usuário a ser buscado",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
                'nome': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do usuário'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail do usuário'),
                'senha': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário'),
                'idade': openapi.Schema(type=openapi.TYPE_INTEGER, description='Idade do usuário'),
                'peso': openapi.Schema(type=openapi.TYPE_NUMBER, description='Peso do usuário'),
                'altura': openapi.Schema(type=openapi.TYPE_NUMBER, description='Altura do usuário'),
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Gênero do usuário'),
                'endereco': openapi.Schema(type=openapi.TYPE_STRING, description='Endereço do usuário'),
                'telefone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone do usuário'),
                'data_nascimento': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Data de nascimento do usuário (formato: YYYY-MM-DD)'),
            },
        required=['nome', 'email', 'senha', 'telefone', 'endereco']
    ),
    responses={
        200: openapi.Response(
            description='Detalhes do paciente atualizado',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'nome': openapi.Schema(type=openapi.TYPE_STRING),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'senha': openapi.Schema(type=openapi.TYPE_STRING),
                    'telefone': openapi.Schema(type=openapi.TYPE_STRING),
                    'endereco': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        404: openapi.Response(
            description="Nenhum paciente com este ID foi encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        ),
        400: openapi.Response(
            description="Erro ao tentar atualizar o paciente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        )
    }
)
    def patch(self, request):
        if request.user.is_paciente:
            try:
                request_body = json.loads(request.body.decode("utf-8"))
                id_paciente = request_body["id_paciente"]
                paciente = Paciente.objects.get(pk=id_paciente)
                serializer = PacienteSerializer(paciente,data=request.data,partial=True) 
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=201, data=serializer.data)
            except Paciente.DoesNotExist:
                return JsonResponse({"error":"Paciente não encontrado."}, status=404)
            except Exception as e:
                return JsonResponse(status=400, data=f"Insira os dados corretamente. {e}")
        return JsonResponse({"Error":"Usuário não é instância de paciente, função não permitida."})
        
class DeletePacienteView(APIView):
    """
    View responsável por deletar um Paciente da base de dados.
    
    Métodos:
        delete(*args, **kwargs): Deleta o Paciente com base no ID fornecido.
    """
    permission_classes = [IsAuthenticated,IsPaciente]
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do usuário a ser buscado",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Paciente deletado.',
        ),
        404: openapi.Response(
            description="Nenhum paciente com este ID foi encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        ),
        400: openapi.Response(
            description="Erro ao tentar deletar o paciente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        )
    }
    def delete(self,request):
        """
        Deleta um Paciente da base de dados com base no ID fornecido.

        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave contendo o ID do Paciente.

        Returns:
            JsonResponse: Confirmação de deleção ou mensagem de erro em caso de falha.
        """
        if request.user.is_paciente:
            try:
                request_body = json.loads(request.body.decode("utf-8"))
                paciente_id = request_body["id_paciente"]
                paciente = Paciente.objects.get(pk=paciente_id)
                paciente.delete()
                return JsonResponse("Paciente deletado com sucesso.",status=200,safe=False)
            except Paciente.DoesNotExist:
                return JsonResponse({'status': 'erro', 'mensagem': f'Nenhum Paciente com este id foi encontrado.'}, status=404)
            except Exception as e:
                return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)
        return JsonResponse({"error":"Usuário não é instância de paciente."})


class AdicionaAlimentoNoDiarioView(APIView):
    permission_classes = [IsAuthenticated,IsPaciente]
    """
    View responsável por atualizar as informações do diario alimentar do paciente.

    Métodos:
        patch(request): Atualiza os dados do diario alimentar com base no token do usuário e os dados fornecidos na request.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_paciente": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID do paciente"
                ),
                "diario_alimentar":openapi.Schema(
                    type=openapi.TYPE_OBJECT, description="Diário alimentar do paciente."
                )
            },
        ),
        responses={
            200: openapi.Response(
                description="Detalhes do diário alimentar atualizado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "nome": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "senha": openapi.Schema(type=openapi.TYPE_STRING),
                        "telefone": openapi.Schema(type=openapi.TYPE_STRING),
                        "endereco": openapi.Schema(type=openapi.TYPE_STRING),
                        "diario_alimentar":openapi.Schema(type=openapi.TYPE_OBJECT)
                    },
                ),
            ),
            404: openapi.Response(
                description="Nenhum paciente foi encontrado.",
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
                description="Erro ao tentar atualizar o diario alimentar.",
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
        if request.user.is_paciente:
            try:
                request_body = json.loads(request.body.decode("utf-8"))
                id_paciente = request_body["id_paciente"]
                paciente = get_object_or_404(Paciente,pk=id_paciente)
                serializer = PacienteSerializer(paciente,data=request.data,partial=True)
                diario_alimentar = request.data.get("diario_alimentar")
                if serializer.is_valid() and diario_alimentar:
                    serializer.save()
                    paciente.save()
                    return JsonResponse(status=201, data=serializer.data)
            except Paciente.DoesNotExist:
                return JsonResponse({"error":"Paciente não encontrado."}, status=404)
            except Exception as e:
                return JsonResponse(status=400, data=f"Insira os dados corretamente. {e}",safe=False)
        return JsonResponse({"Error":"Usuário não é instância de paciente, função não autorizada."})

