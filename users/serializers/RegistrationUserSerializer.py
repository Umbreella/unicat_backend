from django.core.exceptions import ValidationError as djValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import User
from ..tasks.SendConfirmEmailTask import send_confirm_email_task
from .LoginUserSerializer import LoginUserSerializer


class RegistrationUserSerializer(LoginUserSerializer):
    first_name = serializers.CharField(required=True, write_only=True,
                                       max_length=128)
    last_name = serializers.CharField(required=True, write_only=True,
                                      max_length=128)
    refresh = None
    access = None

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except djValidationError:
            detail = {
                'email': [
                    'This email is already registered.',
                ],
            }
            raise ValidationError(detail)

        send_confirm_email_task.apply_async(kwargs={
            'user_email': user.email,
        })

        return user
