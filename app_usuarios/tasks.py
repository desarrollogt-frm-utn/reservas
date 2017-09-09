# coding=utf-8

import base64
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from django.conf import settings


@shared_task(name='enviar_mail_registro')
def enviarMailRegistro(email):
    # Se genera token con email del usuario.
    email_encoded = base64.b64encode(email.encode('utf-8'))

    # Creación de URL de confirmación
    confirm_url = settings.SITE_URL + 'cuentas/signup/' + email_encoded.decode('utf-8')

    # Obtención de templates html y txt de emails.
    htmly = loader.get_template('app_usuarios/email/html/register.html')
    text = loader.get_template('app_usuarios/email/txt/register.txt')

    # Definición de variables de contexto
    variables = {
        'confirm_url': confirm_url,
    }
    html_content = htmly.render(variables)
    text_content = text.render(variables)

    # Creación y envío de email.
    msg = EmailMultiAlternatives(
        'Bienvenido al sistema de Reservas-FRM-UTN',
        text_content,
        to=[email]
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
