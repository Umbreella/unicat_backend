import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from unicat.graphql.functions import get_value_from_model_id

from ..models.UserCourse import UserCourse


class UserCertificateType(DjangoObjectType):
    course = graphene.String()
    title = graphene.String()
    created_at = graphene.String()

    class Meta:
        model = UserCourse
        interfaces = (relay.Node,)
        fields = ('id',)

    def resolve_course(self, info):
        global_course_id = get_value_from_model_id('CourseType',
                                                   self.course_id)
        return global_course_id

    def resolve_title(self, info):
        return str(self.course)

    def resolve_created_at(self, info):
        return self.completed_at.strftime('%d.%m.%Y')


class AuthCertificateConnection(relay.Connection):
    class Meta:
        node = UserCertificateType


class UserCertificateQuery(graphene.ObjectType):
    my_certificates = relay.ConnectionField(AuthCertificateConnection)

    @login_required
    def resolve_my_certificates(root, info, **kwargs):
        user = info.context.user

        data = user.my_progress.filter(**{
            'completed_at__isnull': False,
        })

        return data
