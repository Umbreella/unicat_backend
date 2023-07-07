import jwt
from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task(base=Singleton)
def send_confirm_email_task(user_id: int, user_email: str):
    token = jwt.encode(**{
        'payload': {
            'user_id': user_id,
        },
        'key': settings.SECRET_KEY,
        'algorithm': 'HS256',
    })

    url = f'{settings.MAIN_HOST}/email/confirm/{token}'
    html = render_to_string('ConfirmEmail.html', {'url': url})
    body = (
        'Hi,',
        'To complete registration, you must confirm your email!',
        (
            'Please click this link to confirm your email (this link is '
            'only active for 10 minutes):'
        ),
        f'\n\n{url}\n\n',
        'If you did not make this then please ignore this email.',
    )

    send_mail(**{
        'subject': 'Please confirm your email',
        'message': '\n'.join(body),
        'from_email': settings.EMAIL_HOST_USER,
        'recipient_list': (user_email,),
        'html_message': html,
    })

    return 'Email is sent.'
