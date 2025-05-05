import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.nutricionista import Nutricionista
from ..models.paciente import Paciente
from ..serial import PlanoAlimentarSerializer
from utils.gerar_plano import gerar_pdf
from utils.user_permissions import IsNutricionista
class CriarPlanoAlimentarView(APIView):
    permission_classes = [IsAuthenticated,IsNutricionista]
    def post(self,request):
        if request.user.is_nutricionista:
            try:
                request_body = json.loads(request.body.decode("utf-8"))
                id_nutricionista = request_body["id_nutricionista"]
                nutricionista = get_object_or_404(Nutricionista,pk=id_nutricionista)
                paciente = request_body["paciente"]
                plano_data = {
                    'nutricionista':nutricionista.id,
                    'paciente':paciente,
                    'dados_json':request.data["dados_json"]
                }
                serializer = PlanoAlimentarSerializer(data=plano_data)
                if serializer.is_valid():
                    plano = serializer.save()
                    gerar_pdf(plano)
                    return Response("Sucesso! Seu plano alimentar foi gerado.",status=status.HTTP_200_OK)
            except Nutricionista.DoesNotExist:
                return Response({"error": "Nutricionista não encontrado."}, status.HTTP_404)
            except Paciente.DoesNotExist:
                return Response({'error':"Paciente não encontrado."},status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error":"Usuário não é instância de nutricionista, função não autorizada."},status=status.HTTP_400_BAD_REQUEST)