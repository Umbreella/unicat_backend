from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task(base=Singleton)
def send_confirmed_email_task(user_email: str):
    url = f'{settings.MAIN_HOST}/courses'
    html = render_to_string('SuccessRegistration.html', {'url': url})
    body = (
        'Hi,',
        (
            'You have successfully registered on the Unicat website. '
            'Now you can start learning!'
        ),
        'Click on the link to view the courses:',
        f'\n\n{url}\n\n',
    )

    send_mail(**{
        'subject': 'Your registration is complete',
        'message': '\n'.join(body),
        'from_email': settings.EMAIL_HOST_USER,
        'recipient_list': (user_email,),
        'html_message': html,
    })

    return 'Email is sent.'
