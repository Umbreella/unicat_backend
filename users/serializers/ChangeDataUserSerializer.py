from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as djValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ChangeDataUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(write_only=True, max_length=128)
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        new_email = validated_data.get('email', instance.email)
        if instance.email != new_email:
            instance.email = new_email

        new_password = validated_data.get('password', None)
        if new_password:
            instance.password = make_password(new_password)

        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)

        try:
            instance.save()
        except djValidationError as _raise:
            raise ValidationError(_raise)

        return instance
