import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from jwt import DecodeError
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.serializers import CharField, Serializer

from ..models import User
from ..tasks.SendConfirmedEmailTask import send_confirmed_email_task


class ConfirmEmailSerializer(Serializer):
    url = CharField(min_length=100, max_length=255)

    def validate(self, attrs):
        try:
            decoded_data = jwt.decode(**{
                'jwt': attrs['url'],
                'key': settings.SECRET_KEY,
                'algorithms': ('HS256',),
            })
        except DecodeError:
            detail = {
                'url': 'This field is not valid.',
            }
            raise ValidationError(detail)

        try:
            self.user = User.objects.using(
                'master'
            ).get(**{
                'email': decoded_data['user_email'],
            })
        except ObjectDoesNotExist:
            raise AuthenticationFailed('User not found.')

        if self.user.is_active:
            raise AuthenticationFailed('User already verified.')

        return decoded_data

    def save(self, **kwargs):
        self.user.is_active = True
        self.user.save()

        send_confirmed_email_task.apply_async(kwargs={
            'user_email': self.user.email,
        })

        return self.user
