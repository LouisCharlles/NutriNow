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

def enviar_email_consulta_confirmada(paciente_email, consulta_data, consulta_nutricionista):
    assunto = "Confirmação de Consulta NutriNow"
    mensagem = f"Olá! Sua consulta está confirmada para {consulta_data} com o(a) profissional: {consulta_nutricionista}."

    email = EmailMessage(
        assunto,
        mensagem,
        "NutriNow <Luiscmacedo84@gmail.com>",
        [paciente_email],
    )
    email.send(fail_silently=False)