import json
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ..models import Paciente,Nutricionista,Consulta,Usuario
from ..serial import ConsultaSerializer
from django.http import JsonResponse
from utils.user_permissions import IsNutricionista,IsPaciente
class PacienteMarcaConsultaView(APIView):
    """
    View para marcar uma consulta entre um paciente e um nutricionista específico.
    
    Métodos:
        post(request): Marca a consulta com base no token do paciente.
    """
    permission_classes = [IsAuthenticated,IsPaciente]
    @swagger_auto_schema(
    operation_summary="Marcar uma nova consulta",
    operation_description="Permite que um paciente marque uma consulta com um nutricionista específico usando o ID do nutricionista e a data desejada.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['nutricionista', 'data_consulta'],
        properties={
            'nutricionista': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID do nutricionista"),
            'data_consulta': openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Data e hora da consulta no formato ISO 8601")
        }
    ),
    responses={
        201: openapi.Response("Consulta marcada com sucesso", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'data_consulta': openapi.Schema(type=openapi.TYPE_STRING),
                'nutricionista': openapi.Schema(type=openapi.TYPE_INTEGER),
                'paciente': openapi.Schema(type=openapi.TYPE_INTEGER),
                'realizada': openapi.Schema(type=openapi.TYPE_BOOLEAN)
            }
        )),
        400: "Erro na requisição",
        404: "Nutricionista ou paciente não encontrado"
    }
)
    def post(self,request):
        """
        Função para marcar uma consulta entre um paciente e um nutricionista específico a partir do token do usuário logado na sessão, id não é necessário se você está logado no momento.

        Args:
            request (HttpRequest): Objeto da requisição contendo os ID do nutricionista.
            
        Returns:
            JsonResponse: Detalhes da consulta criada ou mensagem de erro em caso de falha.
        """
        usuario = request.user
        if usuario.is_paciente:
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
        else:
            return JsonResponse({"error":"Usuário não é paciente, não é permitido realizar esta função."})
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
        try:
            id_consulta = kwargs["pk"]
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
    permission_classes = [IsAuthenticated,IsNutricionista]
    @swagger_auto_schema(
    operation_summary="Marcar consulta como realizada",
    operation_description="Permite que um nutricionista atualize o status de uma consulta para 'realizada'.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id_consulta', 'realizada'],
        properties={
            'id_consulta': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID da consulta"),
            'realizada': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Status a ser definido como True")
        }
    ),
    responses={
        200: openapi.Response("Consulta atualizada com sucesso", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'realizada': openapi.Schema(type=openapi.TYPE_BOOLEAN)
            }
        )),
        404: "Consulta não encontrada",
        400: "Erro ao atualizar status da consulta"
    }
)
    def patch(self,request):
        """
        Atualiza o status da consulta para realizada.

        Parâmetros:
        - request (HttpRequest): Requisição HTTP contendo os dados da consulta.
        
        Retornos:
        - JsonResponse: Confirmação de atualização ou mensagem de erro.
        """
        usuario = request.user
        if usuario.is_nutricionista:
            try:
                body = json.loads(request.body.decode("utf-8"))
                consulta_id= body["id_consulta"]
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
        else:
            return JsonResponse({"Error":"Usuário não é nutricionista, não é permitido realizar essa função."})

class VizualizarListaDeConsultasView(APIView):
    permission_classes = [IsAuthenticated]
    """
    View responsável por visualizar a lista de consultas de um nutricionista.
    """
    @swagger_auto_schema(
    operation_summary="Listar consultas pendentes",
    operation_description="Retorna a lista de todas as consultas marcadas, realizadas ou não com um nutricionista. O usuário deve estar autenticado para retornar suas consultas.",
    responses={
        200: openapi.Response("Lista de consultas pendentes", openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'data_consulta': openapi.Schema(type=openapi.TYPE_STRING),
                    'nutricionista_nome': openapi.Schema(type=openapi.TYPE_STRING),
                    'paciente_nome': openapi.Schema(type=openapi.TYPE_STRING),
                    'realizada': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        )),
        404: "Nutricionista ou consultas não encontradas",
        400: "Erro ao processar requisição"
    }
)
    def get(self,request,*args,**kwargs):
        if request.user.is_nutricionista:
            try:
                nutricionista = Nutricionista.objects.get(pk=kwargs["pk"])
                consultas = Consulta.objects.filter(nutricionista=nutricionista).values(
                    'id', 'data_consulta', 'nutricionista__nome', 'paciente__nome', 'realizada'
                )
                lista_consultas = []
                for consulta in consultas:       
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
        elif request.user.is_paciente:
            try:
                paciente = Paciente.objects.get(pk=kwargs["pk"])
                consultas = Consulta.objects.filter(paciente=paciente).values(
                    'id', 'data_consulta', 'nutricionista__nome', 'paciente__nome', 'realizada'
                )
                lista_consultas = []
                for consulta in consultas:       
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

        return JsonResponse({"Error": "Usuário não é nutricionista ou Paciente, não é permitido realizar essa função."})
