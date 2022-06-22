from django.core.mail import EmailMessage
from django.template.loader import get_template


def send_welcome_email(name, email):
    message = get_template('welcome.html').render(context=({'name': name}))
    mail = EmailMessage(
        subject='Welcome to the Jungle.',
        body=message,
        to=[email],
    )
    mail.content_subtype = 'html'
    return mail.send(fail_silently=False)


def send_otp_email(name, email, otp):
    message = get_template('otp.html').render(context=({'name': name, 'otp': otp}))
    mail = EmailMessage(
        subject='The best subject for a OTP mail.',
        body=message,
        to=[email],
    )
    mail.content_subtype = 'html'
    return mail.send(fail_silently=False)
