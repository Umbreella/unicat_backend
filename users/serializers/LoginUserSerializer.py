from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True,
                                   max_length=128)
    password = serializers.CharField(required=True, write_only=True,
                                     max_length=128)
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    def validate(self, attrs):
        user = authenticate(**attrs)

        if not user:
            raise AuthenticationFailed('User not found.')

        setattr(self, 'user', user)

        return attrs

    def get_refresh(self, obj):
        user = self.user

        self.refresh = RefreshToken.for_user(user)
        self.refresh['is_staff'] = user.is_staff

        return str(self.refresh)

    def get_access(self, obj):
        return str(self.refresh.access_token)
