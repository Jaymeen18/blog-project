from django.core.mail import send_mail,EmailMessage
from django.conf import settings


def sent_email_to_client(request):
    subject ='This email is from django server'
    message='This is a email verifiction email'
    from_email = settings.EMAIL_HOST_USER
    recipint_list= ['jaymeen@yopmail.com']
    send_mail(subject,message,from_email,recipint_list)

    send_mail()


def send_email_with_attachement(request,subject,message,recipint_list,file_path):
    mail = EmailMessage(subject=subject,body=message,from_email=settings.EMAIL_HOST_USER,
                        to=recipint_list)
    mail.attach_file(file_path)
    mail.send()
    