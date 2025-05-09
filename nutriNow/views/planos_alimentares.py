import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.nutricionista import Nutricionista
from ..models.paciente import Paciente
from ..models.plano_alimentar import PlanoAlimentar
from ..serial import PlanoAlimentarSerializer
from utils.gerar_plano import gerar_pdf
from utils.user_permissions import IsNutricionista
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
class CriarPlanoAlimentarView(APIView):
    permission_classes = [IsAuthenticated,IsNutricionista]
    def post(self,request):
        if request.user.is_nutricionista:
            try:
                request_body = json.loads(request.body.decode("utf-8"))
                id_nutricionista = request_body["id_nutricionista"]
                nutricionista = get_object_or_404(Nutricionista,pk=id_nutricionista)
                paciente_id = request_body["paciente"]
                plano_data = {
                    'nutricionista':nutricionista.id,
                    'paciente':paciente_id,
                    'dados_json':request.data["dados_json"]
                }
                serializer = PlanoAlimentarSerializer(data=plano_data)
                if serializer.is_valid():
                    plano = serializer.save()
                    gerar_pdf(plano)
                    return Response(f"Id - {serializer.data["id"]}",status=status.HTTP_200_OK)
            except Nutricionista.DoesNotExist:
                return Response({"error": "Nutricionista não encontrado."}, status.HTTP_404)
            except Paciente.DoesNotExist:
                return Response({'error':"Paciente não encontrado."},status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error":"Usuário não é instância de nutricionista, função não autorizada."},status=status.HTTP_400_BAD_REQUEST)

class GetPlanoAlimentarInfoView(APIView):
    """
    View para buscar as informações de um paciente pelo seu ID.
    
    Métodos:
        get(*args, **kwargs): Retorna os detalhes do paciente baseado no id.
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do plano alimentar a ser buscado",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200:openapi.Response('Detalhes do plano alimentar',openapi.Schema(type=openapi.TYPE_OBJECT,properties={
            'id':openapi.Schema(type=openapi.TYPE_INTEGER),
            'paciente_id':openapi.Schema(type=openapi.TYPE_INTEGER),
            'nutricionista_id':openapi.Schema(type=openapi.TYPE_INTEGER),
            "Dados_json":openapi.Schema(type=openapi.TYPE_OBJECT),
        })),
        404:'Nenhum plano alimentar com este id foi encontrado.',
        400: 'Erro na requisição.'
    })
    def get(self,*args,**kwargs):
        """
        Retorna os detalhes de um paciente específico com base no Token.
        
        Returns:
            JsonResponse: Informações do paciente se encontrado ou mensagem de erro caso contrário.
        """
        try:
            plano_id = kwargs["pk"]
            plano = PlanoAlimentar.objects.get(pk=plano_id)
            serializer = PlanoAlimentarSerializer(plano)
            return Response(serializer.data["dados_json"], status=200)
        except PlanoAlimentar.DoesNotExist:
            return Response({"error": "Plano alimentar não encontrado."}, status=404)
        except Paciente.DoesNotExist:
            return Response({"error": "Paciente não encontrado."}, status=404)
        except Nutricionista.DoesNotExist:
            return Response({"error": "Nutricionista não encontrado."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)