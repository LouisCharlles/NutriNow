from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..serial import RegistroUsuarioSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Paciente,Nutricionista
class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]
    """
    View responsável por criar um novo usuário na aplicação.
    
    Métodos:
        post(request): Cria um novo usuário baseado nos dados fornecidos no corpo da requisição.
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nome de usuário'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                'is_paciente': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Se é paciente'),
                'is_nutricionista': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Se é nutricionista'),

                # paciente_data
                'paciente_data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nome': openapi.Schema(type=openapi.TYPE_STRING),
                        'idade': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'peso': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'altura': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'genero': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                        'senha': openapi.Schema(type=openapi.TYPE_STRING),
                        'endereco': openapi.Schema(type=openapi.TYPE_STRING),
                        'telefone': openapi.Schema(type=openapi.TYPE_STRING),
                        'data_nascimento': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    },
                    description="Dados do paciente (se is_paciente=True)",
                    required=['nome', 'idade', 'peso', 'altura', 'genero', 'email', 'senha', 'endereco', 'telefone', 'data_nascimento']
                ),

                # nutricionista_data
                'nutricionista_data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nome': openapi.Schema(type=openapi.TYPE_STRING),
                        'idade': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'peso': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'altura': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'genero': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                        'senha': openapi.Schema(type=openapi.TYPE_STRING),
                        'endereco': openapi.Schema(type=openapi.TYPE_STRING),
                        'telefone': openapi.Schema(type=openapi.TYPE_STRING),
                        'data_nascimento': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    },
                    description="Dados do nutricionista (se is_nutricionista=True)",
                    required=['nome', 'idade', 'peso', 'altura', 'genero', 'email', 'senha', 'endereco', 'telefone', 'data_nascimento']
                ),
            },
            required=['username', 'email', 'password']
        ),
        responses={
            201: openapi.Response('Usuário criado com sucesso.'),
            400: openapi.Response('Erro na requisição.')
        }
    )
    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            if request.data['is_paciente']:
                user = serializer.save()
                paciente = Paciente.objects.filter(email__iexact=user.email).values('id','nome','email','senha').first()
                return Response({'mensagem': f'Usuário criado com sucesso! id:{paciente['id']}'}, status=status.HTTP_201_CREATED)
            elif request.data['is_nutricionista']:
                user = serializer.save()
                nutricionista = Nutricionista.objects.filter(email__ixact=user.email).values('id','nome','email','senha').first()
                return Response({'mensagem': f'Usuário criado com sucesso! id:{nutricionista['id']}'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)