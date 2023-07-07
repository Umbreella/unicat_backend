import re

import jwt
from django.conf import settings
from django.core import mail
from django.test import TestCase

from ...tasks.SendConfirmEmailTask import send_confirm_email_task


class SendConfirmEmailTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = send_confirm_email_task

    def test_When_TaskIsCalled_Should_CreateMailForConfirmEmail(self):
        task = self.tested_task.apply_async(kwargs={
            'user_id': 1,
            'user_email': 'test@test.com',
        })

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Email is sent.'
        real_result = str(task.result)

        _mail = mail.outbox[0]

        expected_mail_subject = 'Please confirm your email'
        real_mail_subject = _mail.subject

        expected_token_payload = {
            'user_id': 1,
        }
        real_token_payload = jwt.decode(**{
            'jwt': re.findall(r'\w*[.]\w*[.]\w*', _mail.body)[0],
            'key': settings.SECRET_KEY,
            'algorithms': ['HS256', ],
        })

        expected_mail_from_email = settings.EMAIL_HOST_USER
        real_mail_from_email = _mail.from_email

        expected_mail_recipients = ['test@test.com', ]
        real_mail_recipients = _mail.recipients()

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_mail_subject, real_mail_subject)
        self.assertEqual(expected_token_payload, real_token_payload)
        self.assertEqual(expected_mail_from_email, real_mail_from_email)
        self.assertEqual(expected_mail_recipients, real_mail_recipients)
