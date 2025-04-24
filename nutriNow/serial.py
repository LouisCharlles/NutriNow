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
    email = serializers.EmailField(required=True)
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
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if not attrs.get('is_paciente') and not attrs.get('is_nutricionista'):
            raise serializers.ValidationError("É necessário informar se é paciente ou nutricionista.")
        # valida a senha com os validadores do Django
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

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
                'nome': nutricionista_data.get('nome', user.username),
                'senha': nutricionista_data.get('senha'),
                'email': user.email,
                'telefone': nutricionista_data.get('telefone'),
                'endereco': nutricionista_data.get('endereco')
            }
            Nutricionista.objects.create(**nutricionista_data)

        return user
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            'id', 'usuario', 'nome', 'email', 'idade', 'peso', 'altura',
            'endereco', 'genero', 'telefone', 'data_nascimento', 'diario_alimentar'
        ]

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
        fields = ['id', 'usuario','nome', 'email', 'senha','endereco', 'telefone']

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