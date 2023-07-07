from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task(base=Singleton)
def send_reset_password_email_task(password_url: str, user_email: str):
    url = f'{settings.MAIN_HOST}/password/reset/{password_url}'
    html = render_to_string('ResetPassword.html', {'url': url})
    body = (
        'Hi,',
        'There was a request to change your password!',
        (
            'Please click this link to change your password (this '
            'link is only active for 10 minutes):'
        ),
        f'\n\n{url}\n\n',
        'If you did not make this request then ignore this email.',
    )

    send_mail(**{
        'subject': 'Please reset your password',
        'message': '\n'.join(body),
        'from_email': settings.EMAIL_HOST_USER,
        'recipient_list': (user_email,),
        'html_message': html,
    })

    return 'Email is sent.'
