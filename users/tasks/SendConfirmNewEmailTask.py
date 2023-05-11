from celery import shared_task
from celery_singleton import Singleton
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task(base=Singleton)
def send_confirm_new_email_task(email_url: int, user_email: str):
    url = f'http://localhost:3000/email/change/{email_url}'
    html = render_to_string('ChangeEmail.html', {'url': url})
    body = (
        'Hi,',
        'There was a request to change your email!',
        (
            'Please click this link to confirm your email (this link '
            'is only active for 10 minutes):'
        ),
        f'\n\n{url}\n\n',
        'If you did not make this request then ignore this email.',
    )

    send_mail(**{
        'subject': 'Please confirm your new email',
        'message': '\n'.join(body),
        'from_email': user_email,
        'recipient_list': (user_email,),
        'html_message': html,
    })
