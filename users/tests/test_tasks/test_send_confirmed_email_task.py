from django.conf import settings
from django.core import mail
from django.test import TestCase

from ...tasks.SendConfirmedEmailTask import send_confirmed_email_task


class SendConfirmEmailTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = send_confirmed_email_task

    def test_When_TaskIsCalled_Should_CreateMailForViewCourses(self):
        task = self.tested_task.apply_async(kwargs={
            'user_email': 'test@test.com',
        })

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Email is sent.'
        real_result = str(task.result)

        _mail = mail.outbox[0]

        expected_mail_subject = 'Your registration is complete'
        real_mail_subject = _mail.subject

        expected_mail_body = '\n'.join((
            'Hi,',
            (
                'You have successfully registered on the Unicat website. '
                'Now you can start learning!'
            ),
            'Click on the link to view the courses:',
            '\n\nhttp://localhost:3000/courses\n\n',
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
