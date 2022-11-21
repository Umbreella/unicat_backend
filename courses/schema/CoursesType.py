import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.Course import Course


class CoursesType(DjangoObjectType):
    class Meta:
        model = Course
        interfaces = (relay.Node, )
        fields = "__all__"

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)


class CoursesConnection(relay.Connection):
    class Meta:
        node = CoursesType


class CourseQuery(graphene.ObjectType):
    course = relay.Node.Field(CoursesType)
    all_courses = relay.ConnectionField(CoursesConnection)

    def resolve_all_courses(root, info, **kwargs):
        return Course.objects.all()
