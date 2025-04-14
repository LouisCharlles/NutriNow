from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Nutricionista
from ..serial import NutricionistaSerializer
from django.http import JsonResponse
class GetNutricionistaInfoView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do nutricionista a ser buscado",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200:openapi.Response('Detalhes do nutricionista',openapi.Schema(type=openapi.TYPE_OBJECT,properties={
            'id':openapi.Schema(type=openapi.TYPE_INTEGER),
            'nome':openapi.Schema(type=openapi.TYPE_STRING),
            'email':openapi.Schema(type=openapi.TYPE_STRING),
            "senha":openapi.Schema(type=openapi.TYPE_STRING),
            'endereco':openapi.Schema(type=openapi.TYPE_STRING),
            'telefone':openapi.Schema(type=openapi.TYPE_STRING),
        })),
        404:'Nenhum nutricionista com este id foi encontrado.',
        400: 'Erro na requisição.'
    })
    def get(self,*args,**kwargs):
        """
        Retorna os detalhes de um nutricionista específico com base no id.
        
        Returns:
            JsonResponse: Informações do nutricionista se encontrado ou mensagem de erro caso contrário.
        """
        try:
            nutricionista_id = kwargs["pk"]
            nutricionista = Nutricionista.objects.get(pk=nutricionista_id)
            serializer = NutricionistaSerializer(nutricionista)
            return Response(serializer.data, status=200)
        except Nutricionista.DoesNotExist:
            return Response({"error": "Nutricionista não encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)
        
class UpdateNutricionistaView(APIView):
    """
    View responsável por atualizar as informações de um nutricionista existente.
    
    Métodos:
        patch(request): Atualiza os dados do nutricionista com base no token do nutricionista e os dados fornecidos na request.
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do nutricionista a ser buscado",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
                'nome': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do nutricionista'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail do nutricionista'),
                'senha': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do nutricionista'),
                'endereco': openapi.Schema(type=openapi.TYPE_STRING, description='Endereço do nutricionista'),
                'telefone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone do nutricionista'),
            },
    ),
    responses={
        200: openapi.Response(
            description='Detalhes do nutricionista atualizado',
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
            description="Nenhum nutricionista foi encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        ),
        400: openapi.Response(
            description="Erro ao tentar atualizar o nutricionista.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        )
    }
)
    def patch(self, request,*args,**kwargs):
        try:
            nutricionista_id = kwargs["pk"]
            nutricionista = Nutricionista.objects.get(pk=nutricionista_id)
            serializer = NutricionistaSerializer(nutricionista,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(status=201,data=serializer.data)
        except Nutricionista.DoesNotExist:
            return JsonResponse({"error":"Nutricionista não encontrado."}, status=404)
        except Exception as e:
            return JsonResponse(status=400, data=f"Insira os dados corretamente. {e}")

class DeleteNutricionistaView(APIView):
    """
    View responsável por deletar um Nutricionista da base de dados.
    
    Métodos:
        delete(*args, **kwargs): Deleta o Nutricionista com base no ID fornecido.
    """
    permission_classes = [IsAuthenticated]
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
            description='Nutricionista deletado.',
        ),
        404: openapi.Response(
            description="Nenhum nutricionista com este ID foi encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        ),
        400: openapi.Response(
            description="Erro ao tentar deletar o nutricionista.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensagem de erro")
                }
            )
        )
    }
    def delete(self,*args,**kwargs):
        """
        Deleta um Nutricionista da base de dados com base no ID fornecido.

        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave contendo o ID do Nutricionista.

        Returns:
            JsonResponse: Confirmação de deleção ou mensagem de erro em caso de falha.
        """
        try:
            nutricionista_id = kwargs["pk"]
            nutricionista = Nutricionista.objects.get(pk=nutricionista_id)
            nutricionista.delete()
            return JsonResponse("Nutricionista deletado com sucesso.",status=200,safe=False)
        except Nutricionista.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': f'Nenhum nutricionista com este id foi encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)