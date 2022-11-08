from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import User
from .LoginUserSerializer import LoginUserSerializer


class RegistrationUserSerializer(LoginUserSerializer):
    first_name = serializers.CharField(required=True, write_only=True,
                                       max_length=128)
    last_name = serializers.CharField(required=True, write_only=True,
                                      max_length=128)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        try:
            self.user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise ValidationError("Unable to create user, invalid fields: "
                                  "email or username")

        return self.user
