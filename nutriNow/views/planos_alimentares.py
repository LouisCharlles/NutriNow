from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.nutricionista import Nutricionista
from ..models.paciente import Paciente
from ..serial import PlanoAlimentarSerializer
from utils.gerar_plano import gerar_pdf

class CriarPlanoAlimentarView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        try:
            id_nutricionista = kwargs["pk"]
            nutricionista = get_object_or_404(Nutricionista,pk=id_nutricionista)
            paciente = request.data["paciente"]
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