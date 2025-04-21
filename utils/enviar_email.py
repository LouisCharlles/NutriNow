from django.core.mail import EmailMessage

def enviar_email_plano(paciente_email,plano_pdf_path):
    assunto = "Seu Plano Alimentar NutriNow."
    mensagem = "Olá! Seu novo plano alimentar está disponível em anexo."

    email = EmailMessage(
        assunto,
        mensagem,
        "NutriNow <Luiscmacedo84@gmail.com>",
        [paciente_email],
    )

    email.attach_file(plano_pdf_path)
    email.send(fail_silently=False)