from django.shortcuts import render
# from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
# from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers

# Create your views here.
def say_hello(request):
    notify_customers.delay('hello')
    return render(request, "hello.html", {"name": "Hilqia"})


# def say_hello(request):
    # try:
        # send_mail('subject', 'message', 'info@groot.com', ['bob@groot.com'])
        # mail_admins('subject', 'message', html_message='message')
        # message = EmailMessage('subject', 'message', 'info@groot.com', ['bob@groot.com'])
        # message.attach_file('playground/static/images/DodgeChallenger.jpeg')
        # message.send()
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Hilqia'}
    #     )
    #     message.send(['jonathan.groot@gmail.com'])
        
    # except BadHeaderError:
    #     pass
        # raise ValueError('Unaurhorize email has been try!!')
    # return render(request, "hello.html", {"name": "Hilqia"})