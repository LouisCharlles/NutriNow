from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
class Usuario(AbstractUser):
    is_paciente = models.BooleanField(default=False)
    is_nutricionista = models.BooleanField(default=False)
class Paciente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    genero = models.CharField(max_length=10) 
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100,default="senha")
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    plano_alimentar = models.FileField(upload_to="pdfs/",blank=True, null=True)

    def __str__(self):
        return self.nome

class Nutricionista(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100,null=False)
    email = models.EmailField(unique=True,null=False)
    senha = models.CharField(max_length=100,null=False,default="senha")
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
    
class Consulta(models.Model):

    data_consulta = models.DateTimeField(null=True,blank=False)

    nutricionista = models.ForeignKey(Nutricionista,on_delete=models.CASCADE)

    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)

    realizada = models.BooleanField(default=False)

