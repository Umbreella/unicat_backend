import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, Serializer

from ..models.ChangeEmail import ChangeEmail


class ConfirmNewEmailSerializer(Serializer):
    url = CharField(min_length=36, max_length=36)

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

    def create(self, validated_data):
        url = validated_data['url']

        try:
            change_email = ChangeEmail.objects.select_related(
                'user',
            ).get(**{
                'url': url,
                'closed_at__gte': timezone.now(),
            })
        except ObjectDoesNotExist:
            detail = {
                'url': [
                    'Value not found.',
                ],
            }
            raise ValidationError(detail)

        change_email.closed_at = timezone.now()
        change_email.save()

        user = change_email.user
        user.email = change_email.email
        user.save()

        return user
