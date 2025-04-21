from django.db import models

class PlanoAlimentar(models.Model):
    nutricionista = models.ForeignKey('Nutricionista', on_delete=models.CASCADE, related_name="planos_criados",blank=True,null=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name="planos_alimentares",null=True,blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    arquivo_pdf = models.FileField(upload_to='planos/%Y/%m/%d/', blank=True, null=True)

    # Dados estruturados, salvos para reprocessamento ou edição
    dados_json = models.JSONField(default=dict, blank=True)

def __str__(self):
    return f"Plano de {self.paciente.nome} por {self.nutricionista.nome}"



