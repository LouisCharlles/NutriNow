from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import PlanoAlimentar
from .models import Consulta
from .models import Paciente
from .models import Notificacao
from utils.gerar_plano import gerar_pdf
from utils.enviar_email import enviar_email_plano,enviar_email_consulta_confirmada

@receiver(post_save,sender=PlanoAlimentar)
def notificar_paciente_plano(sender,instance,created,**kwargs):
    if created:
        pdf_path = gerar_pdf(instance)
        if pdf_path:
            paciente_email = instance.paciente.email
            enviar_email_plano(paciente_email,pdf_path)

@receiver(post_save,sender=Consulta)
def notificar_paciente_consulta(sender,instance,created,**kwargs):
    if created:
        paciente_email = instance.paciente.email
        consulta_data = instance.data_consulta.strftime("%d/%m/%Y %H:%M")
        consulta_nutricionista = instance.nutricionista.nome
        enviar_email_consulta_confirmada(paciente_email,consulta_data,consulta_nutricionista=consulta_nutricionista)
        print("Email enviado com sucesso!")

@receiver(post_save,sender=Consulta)
def notificar_nutricionista_consulta(sender,instance,created,**kwargs):
    if created:
        Notificacao.objects.create(
            paciente=instance.paciente,
            nutricionista=instance.nutricionista,
            mensagem=f"{instance.paciente.nome} marcou uma nova consulta em {instance.data_consulta.strftime('%d/%m/%Y às %H:%M')}"
        )




