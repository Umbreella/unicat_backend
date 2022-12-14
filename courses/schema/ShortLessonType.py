import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.ShortLesson import ShortLesson


class ShortLessonType(DjangoObjectType):
    class Meta:
        model = ShortLesson
        interfaces = (relay.Node,)
        fields = '__all__'


class ShortLessonConnection(relay.Connection):
    class Meta:
        node = ShortLessonType


class ShortLessonQuery(graphene.ObjectType):
    short_lesson = relay.Node.Field(ShortLessonType)
    all_short_lessons = relay.ConnectionField(ShortLessonConnection)

    def resolve_all_short_lessons(root, info, **kwargs):
        return ShortLesson.objects.all()
