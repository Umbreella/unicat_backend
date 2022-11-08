from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class ChangeDataUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, allow_blank=True)
    password = serializers.CharField(write_only=True, allow_blank=True)
    username = serializers.CharField(write_only=True, allow_blank=True)
    first_name = serializers.CharField(write_only=True, allow_blank=True)
    last_name = serializers.CharField(write_only=True, allow_blank=True)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)

        new_password = validated_data.get('password', None)

        if new_password:
            instance.password = make_password(new_password)

        instance.save()

        return instance
