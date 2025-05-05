from django.db import models
from .paciente import Paciente
from .nutricionista import Nutricionista
class Notificacao(models.Model):

    data_criacao = models.DateTimeField(auto_now_add=True,null=False,blank=False)

    lida = models.BooleanField(default=False)

    nutricionista = models.ForeignKey(Nutricionista,on_delete=models.CASCADE,related_name="notificacoes_recebidas")

    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name="notificacoes_enviadas")

    mensagem = models.TextField()

    def __str__(self):
        return f"Para {self.nutricionista.nome}: {self.mensagem[:30]}..."
    
    def marcar_como_lida(self):
        self.lida = True
        self.save()