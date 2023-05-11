from rest_framework.serializers import EmailField, Serializer

from ..models import User
from ..models.ResetPassword import ResetPassword
from ..tasks.SendResetPasswordEmailTask import send_reset_password_email_task


class ResetPasswordSerializer(Serializer):
    email = EmailField(max_length=128, write_only=True)

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.filter(email=email).first()

        if user is not None:
            reset_password = ResetPassword.objects.create(**{
                'user': user,
            })

            send_reset_password_email_task.apply_async(kwargs={
                'password_url': str(reset_password.url),
                'user_email': user.email,
            })

        return User.objects.none()
