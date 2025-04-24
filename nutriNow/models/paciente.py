from django.db import models
from django.conf import settings

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
    plano_alimentar = models.ForeignKey('PlanoAlimentar',on_delete=models.SET_NULL,related_name="paciente_do_plano",blank=True,null=True)
    diario_alimentar = models.JSONField(default=dict,blank=True,null=True)
    def __str__(self):
        return self.nome