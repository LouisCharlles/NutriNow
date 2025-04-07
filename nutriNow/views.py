from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import json
from .models import Paciente,Nutricionista     
from django.http import JsonResponse
from datetime import datetime
from .serial import PacienteSerializer,NutricionistaSerializer
class CreatePacienteView(APIView):
    """
    View responsável por criar um novo paciente na aplicação.
    
    Métodos:
        post(request): Cria um novo paciente baseado nos dados fornecidos no corpo da requisição.
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do paciente'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail do paciente'),
                'senha': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do paciente'),
                'idade': openapi.Schema(type=openapi.TYPE_INTEGER, description='Idade do paciente'),
                'peso': openapi.Schema(type=openapi.TYPE_NUMBER, description='Peso do paciente'),
                'altura': openapi.Schema(type=openapi.TYPE_NUMBER, description='Altura do paciente'),
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Gênero do paciente'),
                'endereco': openapi.Schema(type=openapi.TYPE_STRING, description='Endereço do paciente'),
                'telefone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone do paciente'),
                'data_nascimento': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Data de nascimento do paciente (formato: YYYY-MM-DD)'),
            },
            required=['nome', 'email', 'senha','idade','genero','telefone','data_nascimento','peso','altura','endereco']
        ),
        responses={
            201: openapi.Response('ID do novo paciente', openapi.Schema(type=openapi.TYPE_INTEGER)),
            400: 'Erro ao criar paciente. Verifique os dados fornecidos.'
        }
    )
    
    def post(self, request):
        """
        Cria um novo paciente na base de dados.
        
        Args:
            request (HttpRequest): Objeto da requisição contendo os dados do novo paciente (nome,email,senha,idade,genero,telefone,data_nascimento).

        Returns:
            JsonResponse: ID do novo paciente se criado com sucesso ou mensagem de erro em caso de falha.
        """

        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            paciente = Paciente.objects.filter(email__iexact=email)

            if paciente.exists():
                return JsonResponse({'error': 'Paciente já existe.'}, status=400)

            serializer = PacienteSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'id': serializer.data['id']}, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)

        except TypeError as error:
            return JsonResponse({
                "Error": "Tentativa de cadastro com credenciais inválidas. Verifique os campos e insira corretamente os dados.",
            }, status=400)

class CreateNutricionistaView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do nutricionista'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail do nutricionista'),
                'senha': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do nutricionista'),
                'endereco': openapi.Schema(type=openapi.TYPE_STRING, description='Endereço do nutricionista'),
                'telefone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone do nutricionista'),
            },
            required=['nome', 'email', 'senha','telefone','endereco']
        ),
        responses={
            201: openapi.Response('ID do novo nutricionista', openapi.Schema(type=openapi.TYPE_INTEGER)),
            400: 'Erro ao criar nutricionista. Verifique os dados fornecidos.'
        }
    )
    def post(self,request):
        """
        Cria um novo nutricionista na base de dados.
        
        Args:
            request (HttpRequest): Objeto da requisição contendo os dados do novo nutricionista (nome,email,senha,telefone,endereco).

        Returns:
            JsonResponse: ID do novo nutricionista se criado com sucesso ou mensagem de erro em caso de falha.
        """
        
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            nutricionista = Nutricionista.objects.filter(email__iexact=email)

            if nutricionista.exists():
                return JsonResponse({'error': 'Nutricionista já existe.'}, status=400)

            serializer = NutricionistaSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'id': serializer.data['id']}, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)

        except TypeError as error:
            return JsonResponse({
                "Error": "Tentativa de cadastro com credenciais inválidas. Verifique os campos e insira corretamente os dados.",
            }, status=400)

class GetPacienteInfoView(APIView):
    """
    View para buscar as informações de um paciente pelo seu ID.
    
    Métodos:
        get(*args, **kwargs): Retorna os detalhes do paciente baseado no ID fornecido.
    """
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do paciente a ser buscado",
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
    def get(self, *args, **kwargs):
        """
        Retorna os detalhes de um paciente específico com base no ID.
        
        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave contendo o ID do usuário.
        
        Returns:
            JsonResponse: Informações do paciente se encontrado ou mensagem de erro caso contrário.
        """

        id_paciente = kwargs["pk"]

        try:
            paciente = Paciente.objects.filter(id=id_paciente).values('id', 'nome', 'email', 'senha').first()
            if paciente:
                return JsonResponse(paciente, status=200)  # safe=True is the default
            else:
                return JsonResponse({'status': 'erro', 'mensagem': 'Nenhum paciente com este id foi encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({f"Error":{e}},status=400)

class GetNutricionistaInfoView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID do paciente a ser buscado",
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
    def get(self, *args, **kwargs):
        """
        Retorna os detalhes de um nutricionista específico com base no ID.
        
        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave contendo o ID do nutricionista.
        
        Returns:
            JsonResponse: Informações do nutricionista se encontrado ou mensagem de erro caso contrário.
        """

        id_nutricionista = kwargs["pk"]
        try:
            nutricionista = Nutricionista.objects.filter(id=id_nutricionista).values('id', 'nome', 'email', 'senha').first()
            if nutricionista:
                return JsonResponse(nutricionista, status=200)  # safe=True is the default
            else:
                return JsonResponse({'status': 'erro', 'mensagem': 'Nenhum nutricionista com este id foi encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({f"Error":{e}},status=400)
class UpdatePacienteView(APIView):
    """
    View responsável por atualizar as informações de um paciente existente.
    
    Métodos:
        put(request, *args, **kwargs): Atualiza os dados do paciente com base no ID fornecido.
    """
    
    @swagger_auto_schema(
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
   
    def patch(self, request,*args,**kwargs):
        id_paciente = kwargs["pk"]
        if not id_paciente:
            return JsonResponse({"error":"Paciente não encontrado."}, status=404)
        
        paciente = Paciente.objects.get(pk=id_paciente)
        serializer = PacienteSerializer(paciente,data=request.data,partial=True) # set partial=True to update a data partially

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(status=201, data=serializer.data)
        return JsonResponse(status=400, data="Insira os dados corretamente.")
    
class UpdateNutricionistaView(APIView):
    """
    View responsável por atualizar as informações de um nutricionista existente.
    
    Métodos:
        put(request, *args, **kwargs): Atualiza os dados do nutricionista com base no ID fornecido.
    """
    @swagger_auto_schema(
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
            description="Nenhum nutricionista com este ID foi encontrado.",
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
        id_nutri = kwargs["pk"]
        if not id_nutri:
            return JsonResponse({"error":"Nutricionista não encontrado."}, status=404)
        
        nutricionista = Nutricionista.objects.get(pk=id_nutri)
        
        serializer = NutricionistaSerializer(nutricionista,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(status=201, data=serializer.data)
        return JsonResponse(status=400, data="Insira os dados corretamente.")
    
