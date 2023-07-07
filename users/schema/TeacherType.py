import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.Teacher import Teacher


class TeacherType(DjangoObjectType):
    full_name = graphene.String()
    photo = graphene.String()

    class Meta:
        model = Teacher
        interfaces = (relay.Node,)
        fields = '__all__'

    def resolve_full_name(self, info):
        return info.context.loaders.user_loader.load(self.user_id)

    def resolve_photo(self, info):
        if self.user.photo:
            return info.context.build_absolute_uri(self.user.photo.url)

        return None


class TeacherConnection(relay.Connection):
    class Meta:
        node = TeacherType


class TeacherQuery(graphene.ObjectType):
    all_teachers = relay.ConnectionField(TeacherConnection)

    def resolve_all_teachers(root, info, **kwargs):
        return Teacher.objects.all()
