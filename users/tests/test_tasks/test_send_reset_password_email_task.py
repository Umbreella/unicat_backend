from django.conf import settings
from django.core import mail
from django.test import TestCase

from ...tasks.SendResetPasswordEmailTask import send_reset_password_email_task


class SendConfirmEmailTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = send_reset_password_email_task

    def test_When_TaskIsCalled_Should_CreateMailForViewCourses(self):
        task = self.tested_task.apply_async(kwargs={
            'password_url': 'test_url',
            'user_email': 'test@test.com',
        })

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Email is sent.'
        real_result = str(task.result)

        _mail = mail.outbox[0]

        expected_mail_subject = 'Please reset your password'
        real_mail_subject = _mail.subject

        expected_mail_body = '\n'.join((
            'Hi,',
            'There was a request to change your password!',
            (
                'Please click this link to change your password (this '
                'link is only active for 10 minutes):'
            ),
            '\n\nhttp://localhost:3000/password/reset/test_url\n\n',
            'If you did not make this request then ignore this email.',
        ))
        real_mail_body = _mail.body

        expected_mail_from_email = settings.EMAIL_HOST_USER
        real_mail_from_email = _mail.from_email

        expected_mail_recipients = ['test@test.com', ]
        real_mail_recipients = _mail.recipients()

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_mail_subject, real_mail_subject)
        self.assertEqual(expected_mail_body, real_mail_body)
        self.assertEqual(expected_mail_from_email, real_mail_from_email)
        self.assertEqual(expected_mail_recipients, real_mail_recipients)
