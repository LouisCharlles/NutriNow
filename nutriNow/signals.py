from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlanoAlimentar
from utils.gerar_plano import gerar_pdf
from utils.enviar_email import enviar_email_plano

@receiver(post_save,sender=PlanoAlimentar)
def notificar_paciente_plano(sender,instance,created,**kwargs):
    if created:
        pdf_path = gerar_pdf(instance)
        if pdf_path:
            paciente_email = instance.paciente.email
            enviar_email_plano(paciente_email,pdf_path)
