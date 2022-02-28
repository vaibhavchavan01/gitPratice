from django.core.mail import send_mail

from django.conf import settings

def forget_password_mail(email, token):
    
    subject = 'forget password link is '
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/resetPasswordLink/{token}/{email}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True