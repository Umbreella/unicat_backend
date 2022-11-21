import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.Teacher import Teacher


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        interfaces = (relay.Node, )
        fields = "__all__"

    full_name = graphene.String()

    def resolve_full_name(self, info):
        return self.user.get_fullname()

    def resolve_photo(self, info):
        return info.context.build_absolute_uri(self.photo.url)


class TeacherConnection(relay.Connection):
    class Meta:
        node = TeacherType


class TeacherQuery(graphene.ObjectType):
    all_teachers = relay.ConnectionField(TeacherConnection)

    def resolve_all_teachers(root, info, **kwargs):
        return Teacher.objects.all()
