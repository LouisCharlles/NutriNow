from django.db import models
from .nutricionista import Nutricionista
from .paciente import Paciente
class Consulta(models.Model):

    data_consulta = models.DateTimeField(null=True,blank=False)

    nutricionista = models.ForeignKey(Nutricionista,on_delete=models.CASCADE)

    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)

    realizada = models.BooleanField(default=False)