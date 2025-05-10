from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Paciente, Nutricionista,Consulta,Usuario,PlanoAlimentar
from django.db import transaction
class RegistroUsuarioSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=False)
    idade = serializers.IntegerField(required=False)
    peso = serializers.FloatField(required=False)
    altura = serializers.FloatField(required=False)
    genero = serializers.CharField(required=False)
    endereco = serializers.CharField(required=False)
    telefone = serializers.CharField(required=False)
    data_nascimento = serializers.DateField(required=False)
    password = serializers.CharField(write_only=True)
    paciente_data = serializers.DictField(write_only=True, required=False)
    nutricionista_data = serializers.DictField(write_only=True, required=False)
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password',
            'is_paciente', 'is_nutricionista',
            'nome','idade', 'peso', 'altura', 'genero',
            'endereco','telefone', 'data_nascimento',
            'paciente_data', 'nutricionista_data',
        ]
        extra_kwargs = {'password':{'write_only': True}}  

    def create(self, validated_data):
        is_paciente = validated_data.pop('is_paciente', False)
        is_nutricionista = validated_data.pop('is_nutricionista', False)
        paciente_data = validated_data.pop('paciente_data', {})
        nutricionista_data = validated_data.pop('nutricionista_data', {})

        with transaction.atomic():
            user = Usuario.objects.create_user(**validated_data)
            user.is_paciente = is_paciente
            user.is_nutricionista = is_nutricionista
            
            if is_paciente:
                try:
                    paciente_data = {
                        'usuario':user,
                        'nome':paciente_data.get("nome"),
                        'email':user.email,
                        'senha':paciente_data.get("senha"),
                        'telefone':paciente_data.get("telefone"),
                        'endereco':paciente_data.get("endereco",""),
                        'idade':paciente_data.get("idade"),
                        'genero':paciente_data.get("genero"),
                        'peso':paciente_data.get("peso"),
                        'altura':paciente_data.get("altura"),
                        'data_nascimento':paciente_data.get("data_nascimento"),
                    }

                    Paciente.objects.create(**paciente_data)
                except Exception as e:
                    raise serializers.ValidationError({"paciente_data":f"Erro ao criar paciente {str(e)}"})
            elif is_nutricionista:
                try:
                    nutricionista_data = {
                        'usuario': user,
                        'nome': user.username,
                        'email':user.email,
                        'senha':nutricionista_data.get("senha"),
                        'telefone': nutricionista_data.get('telefone', ''),
                        'endereco': nutricionista_data.get('endereco', ''),
                        'horarios_disponiveis':nutricionista_data.get('horarios_disponiveis',''),
                    }
                    Nutricionista.objects.create(**nutricionista_data)
                except Exception as e:
                    raise serializers.ValidationError({"nutricionista_data":f"Erro ao processar dados de nutricionista: {str(e)}"})
        user.save()
        return user
    
class CustomTokenObtainPairAndIdSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data =  super().validate(attrs)
        user = self.user
        data["user_id"] = user.id
        data["is_paciente"] = user.is_paciente
        data["is_nutricionista"] = user.is_nutricionista

        if user.is_paciente:
            try:
                paciente = Paciente.objects.get(usuario=user)
                data['paciente_id'] = paciente.id
            except Paciente.DoesNotExist:
                data['paciente_id'] = None
        elif user.is_nutricionista:
            try:
                nutricionista = Nutricionista.objects.get(usuario=user)
                data['nutricionista_id'] = nutricionista.id
            except Nutricionista.DoesNotExist:
                data['nutricionista_id'] = None

        return data

        
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id','nome', 'email', 'senha', 'idade', 'peso', 'altura',
            'endereco', 'genero', 'telefone', 'data_nascimento','plano_alimentar','diario_alimentar']

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Email inválido.")
        return value

    def validate_senha(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
class NutricionistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutricionista
        fields = ['id', 'nome', 'email', 'senha','horarios_disponiveis']

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Email inválido.")
        return value

    def validate_senha(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ['id','data_consulta','nutricionista','paciente','realizada']

class PlanoAlimentarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoAlimentar
        fields = ['id','nutricionista','paciente',
    'dados_json','arquivo_pdf']
        read_only_fields = ['arquivo_pdf']