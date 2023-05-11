from django.contrib.auth.hashers import check_password
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, EmailField, Serializer

from ..models import User
from ..models.ChangeEmail import ChangeEmail
from ..tasks.SendConfirmNewEmailTask import send_confirm_new_email_task


class ProfileSerializer(Serializer):
    email = EmailField(max_length=128)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    photo = Base64ImageField()
    current_password = CharField(min_length=8, max_length=128, write_only=True)
    new_password = CharField(min_length=8, max_length=128, write_only=True)

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')

        if bool(current_password) != bool(new_password):
            detail = {
                'current_password': [
                    'This field must be filled.',
                ],
                'new_password': [
                    'This field must be filled.',
                ],
            }
            raise ValidationError(detail)

        return attrs

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        current_password = validated_data.get('current_password')

        if email and instance.email != email:
            email_is_used = User.objects.filter(**{
                'email': email,
            }).exists()

            if email_is_used:
                detail = {
                    'email': [
                        'You cannot use this email as a new email.',
                    ],
                }
                raise ValidationError(detail)

            new_email = ChangeEmail.objects.create(**{
                'user': instance,
                'email': email,
            })

            send_confirm_new_email_task.apply_async(kwargs={
                'email_url': str(new_email.url),
                'user_email': email,
            })

            del validated_data['email']

        if current_password:
            if check_password(current_password, instance.password):
                instance.password = validated_data.pop('new_password')
                del validated_data['current_password']
            else:
                detail = {
                    'current_password': [
                        'Incorrect password.',
                    ],
                }
                raise ValidationError(detail)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
