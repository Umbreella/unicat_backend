import uuid

from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, Serializer

from ..models.ResetPassword import ResetPassword


class UpdatePasswordSerializer(Serializer):
    url = CharField(min_length=36, max_length=36)
    password = CharField(min_length=8, max_length=128)

    def validate(self, attrs):
        url = attrs['url']

        try:
            uuid.UUID(url)
        except ValueError:
            detail = {
                'url': 'This field is not valid.',
            }
            raise ValidationError(detail)

        return attrs

    def save(self, **kwargs):
        url = self.validated_data['url']
        password = self.validated_data['password']

        reset_password = ResetPassword.objects.filter(**{
            'url': url,
            'closed_at__gte': timezone.now(),
        }).select_related('user').first()

        if reset_password is None:
            detail = {
                'url': [
                    'Active password reset request not found.',
                ],
            }
            raise ValidationError(detail)

        user = reset_password.user

        if user.check_password(password):
            detail = {
                'password': [
                    'This password is already in use.',
                ],
            }
            raise ValidationError(detail)

        reset_password.closed_at = timezone.now()
        reset_password.save()

        user.password = password
        user.save()

        return user
