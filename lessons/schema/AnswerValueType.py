from graphene import relay
from graphene_django import DjangoObjectType

from ..models.AnswerValue import AnswerValue


class AnswerValueType(DjangoObjectType):
    class Meta:
        model = AnswerValue
        interfaces = (relay.Node,)
        fields = (
            'id', 'value',
        )
