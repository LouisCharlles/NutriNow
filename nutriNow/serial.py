from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Paciente, Nutricionista,Consulta,Usuario,PlanoAlimentar
from rest_framework import serializers
class RegistroUsuarioSerializer(serializers.ModelSerializer):
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
            'idade', 'peso', 'altura', 'genero', 'endereco',
            'telefone', 'data_nascimento',
            'paciente_data', 'nutricionista_data',
        ]
        extra_kwargs = {'password':{'write_only': True}}  

    def create(self, validated_data):
        is_paciente = validated_data.pop('is_paciente', False)
        is_nutricionista = validated_data.pop('is_nutricionista', False)
        paciente_data = validated_data.pop('paciente_data', {})
        nutricionista_data = validated_data.pop('nutricionista_data', {})

        user = Usuario.objects.create_user(**validated_data)
        user.is_paciente = is_paciente
        user.is_nutricionista = is_nutricionista
        user.save()

        if is_paciente:
            paciente_data['usuario'] = user
            paciente_data['email'] = user.email
            paciente = Paciente.objects.create(**paciente_data)
        elif is_nutricionista:
            nutricionista_data = {
                'usuario': user,
                'nome': user.username,
                'email': user.email,
                'telefone': paciente_data.get('telefone', ''),
                'endereco': paciente_data.get('endereco', '')
            }
            Nutricionista.objects.create(**nutricionista_data)

        return user
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id','nome', 'email', 'senha', 'idade', 'peso', 'altura',
            'endereco', 'genero', 'telefone', 'data_nascimento',]

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
        fields = ['id', 'nome', 'email', 'senha']

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