import json
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ..models import Paciente,Nutricionista,Consulta
from ..serial import ConsultaSerializer
from django.http import JsonResponse

class PacienteMarcaConsultaView(APIView):
    """
    View para marcar uma consulta entre um paciente e um nutricionista específico.
    
    Métodos:
        post(request): Marca a consulta com base no token do paciente.
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'nutricionista': openapi.Schema(type=openapi.TYPE_INTEGER,description="id do nutricionista"),
        'data_consulta':openapi.Schema(type=openapi.TYPE_STRING,description="data da consulta")
    },
    required=['nutricionista','data_consulta']
    ),
    responses={
        201:openapi.Response("ID da consulta gerada",openapi.Schema(type=openapi.TYPE_INTEGER)),
        404: "Nenhum nutricionista  foi encontrado.",
        400:"Ocorreu um erro ao fazer a requisição."
    })
    def post(self,request):
        """
        Função para marcar uma consulta entre um paciente e um nutricionista específico a partir do token do usuário logado na sessão, id não é necessário se você está logado no momento.

        Args:
            request (HttpRequest): Objeto da requisição contendo os ID do nutricionista.
            
        Returns:
            JsonResponse: Detalhes da consulta criada ou mensagem de erro em caso de falha.
        """
        try:
            body = json.loads(request.body.decode('utf-8'))
            id_nutricionista = body.get("nutricionista")
            data_consulta = body.get("data_consulta")

            nutricionista = Nutricionista.objects.get(pk=id_nutricionista)
           

            consulta_data = {
                "nutricionista": nutricionista.id,
                "data_consulta": data_consulta,
                "paciente": request.user.paciente.id,
                "realizada":False,
            }

            serializer = ConsultaSerializer(data=consulta_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        except Paciente.DoesNotExist:
            return JsonResponse({"error": "Paciente não encontrado."}, status=404)
        except Nutricionista.DoesNotExist:  
            return JsonResponse({"error": "Nutricionista não encontrado."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Erro no corpo da requisição."}, status=400)
class UsuarioVizualizaConsultaView(APIView):
    """
    View para visualizar os detalhes de uma consulta marcada.
    
    Métodos:
        get(request): Retorna os detalhes da consulta com base no id da consulta.
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'id', openapi.IN_PATH,
            description="ID da consulta",
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={
        200: openapi.Response(
            'Detalhes da consulta',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'data_consulta': openapi.Schema(type=openapi.TYPE_STRING),
                    'nutricionista_nome': openapi.Schema(type=openapi.TYPE_STRING),
                    'paciente_nome': openapi.Schema(type=openapi.TYPE_STRING),
                    'realizada': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        ),
        404: "Consulta não encontrada",
        400: "Erro de requisição"
    }
)
    def get(self,*args,**kwargs):
        """
        Retorna os detalhes de uma consulta marcada com base no id da consulta.

        Args:
            Kwargs: Objeto da na url contendo o ID da consulta.

        Returns:
            JsonResponse: Detalhes da consulta ou mensagem de erro em caso de falha.
        """
        id_consulta = kwargs["pk"]
        try:
            consulta = Consulta.objects.filter(id=id_consulta).values('id','data_consulta',"nutricionista__nome","paciente__nome",'realizada').first()
            if not consulta:
                return JsonResponse("Não foi possível encontrar a consulta com esse identificador.",status=404,safe=False)
            return JsonResponse(consulta,status=200,safe=False)
        except Exception as e:
            return JsonResponse(f"Uma exceção foi lançada: {e}",status=400,safe=False)
class DefineConsultaComoRealizadaView(APIView):
    """
    View responsável por definir uma consulta como realizada.

    Métodos:
    - patch(request): Marca a consulta como realizada.

    Exceções:
    - Retorna erro 404 caso a consulta não seja encontrada.
    - Retorna erro 400 em caso de dados inválidos ou exceções.
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID da consulta a ser buscada.",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'realizada':openapi.Schema(type=openapi.TYPE_STRING,description="Consulta a ser definida como realizada.")
    },
    required=['realizada']
    ),
    responses={
        200:  openapi.Response(
            description='Detalhes da consulta foram atualizados.',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'realizada': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        ),
        404: openapi.Response(
            description="Nenhuma consulta com esse id foi encontrada.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        ),
        400: openapi.Response(
            description="Erro ao tentar atualizar os dados da consulta, verifique os campos se estão preenchidos corretamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        )
    }
)
    def patch(self,request,*args,**kwargs):
        """
        Atualiza o status da consulta para realizada.

        Parâmetros:
        - request (HttpRequest): Requisição HTTP contendo os dados da consulta.
        
        Retornos:
        - JsonResponse: Confirmação de atualização ou mensagem de erro.
        """
        try:
            body = json.loads(request.body)
            consulta_id= kwargs["pk"]
            consulta = Consulta.objects.get(pk=consulta_id)
            serializer = ConsultaSerializer(consulta,data=body,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
        except TypeError:
            return JsonResponse("Esse tipo não é aceito no campo: realizada.",status=400)
        except Consulta.DoesNotExist:
            return JsonResponse("Essa consulta não existe.",status=404,safe=False)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400,safe=False)

class VizualizarListaDeConsultasView(APIView):
    permission_classes = [IsAuthenticated]
    """
    View responsável por visualizar a lista de consultas de um nutricionista.
    """
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do nutricionista para buscar as consultas.",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],responses={
        200: openapi.Response(
            description='Lista de consultas não realizadas do nutricionista.',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'data_consulta': openapi.Schema(type=openapi.TYPE_STRING),
                        'paciente_nome': openapi.Schema(type=openapi.TYPE_STRING),
                        'realizada': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            )
        ),
        404: openapi.Response(
            description="Nenhum nutricionista ou consulta encontrada.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        ),
        400: openapi.Response(
            description="Erro ao tentar visualizar a lista de consultas.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        )
    })
    def get(self, *args,**kwargs):
       
        try:
            nutricionista = kwargs["pk"]
            consultas = Consulta.objects.filter(nutricionista=nutricionista).values('id','data_consulta','nutricionista__nome','paciente__nome','realizada')

            lista_consultas = []
            for consulta in consultas:
                if not consulta['realizada']:
                    lista_consultas.append({
                        'id': consulta['id'],
                        'data_consulta': consulta['data_consulta'],
                        'nutricionista_nome': consulta['nutricionista__nome'],
                        'paciente_nome': consulta['paciente__nome'],
                        'realizada': consulta['realizada']
                    })
            return JsonResponse(lista_consultas, status=200, safe=False)    
        
        except Paciente.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Paciente não encontrado'}, status=404)
        except Nutricionista.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Nutricionista não encontrado'}, status=404)
        except Consulta.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Nenhuma consulta encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)