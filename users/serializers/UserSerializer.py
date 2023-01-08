from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj)

    def get_photo(self, obj):
        short_url = obj.photo.url
        request = self.context.get('request')

        return request.build_absolute_uri(short_url)
