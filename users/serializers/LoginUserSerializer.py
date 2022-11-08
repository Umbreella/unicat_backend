from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import RefreshToken


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True,
                                   max_length=128)
    password = serializers.CharField(required=True, write_only=True,
                                     max_length=128)
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        self.user = authenticate(email=email, password=password)

        if not self.user:
            raise NotFound("User not found.")

        return attrs

    def get_refresh(self, obj):
        self.refresh = RefreshToken.for_user(self.user)
        return str(self.refresh)

    def get_access(self, obj):
        return str(self.refresh.access_token)
