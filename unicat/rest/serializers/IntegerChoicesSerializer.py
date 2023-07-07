from rest_framework.serializers import CharField, IntegerField, Serializer


class IntegerChoicesSerializer(Serializer):
    id = IntegerField()
    label = CharField()
