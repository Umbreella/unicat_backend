import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from ..filtersets.UserCourseFilterSet import \
    UserCourseFilterSet as UsCourseFilterSet
from ..models.UserCourse import UserCourse
from .CourseType import CourseType


class UserCourseQuery(graphene.ObjectType):
    my_course = graphene.Field(CourseType, id=graphene.ID(required=True))
    my_courses = DjangoFilterConnectionField(CourseType,
                                             filterset_class=UsCourseFilterSet)

    @login_required
    def resolve_my_course(root, info, **kwargs):
        user = info.context.user
        course_id = kwargs.get('id')

        course = relay.Node.get_node_from_global_id(info, course_id)
        has_access = UserCourse.objects.filter(**{
            'course': course,
            'user': user,
        }).exists()

        if not has_access:
            detail = 'You don`t have access on this course.'
            raise GraphQLError(detail)

        return course

    @login_required
    def resolve_my_courses(root, info, **kwargs):
        user = info.context.user

        return user.my_courses.all()
