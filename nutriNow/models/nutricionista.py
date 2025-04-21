from django.db import models
from django.conf import settings

class Nutricionista(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100,null=False)
    email = models.EmailField(unique=True,null=False)
    senha = models.CharField(max_length=100,null=False,default="senha")
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome