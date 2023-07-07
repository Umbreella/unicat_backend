import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene import relay
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_relay import from_global_id

from ..models.CourseStat import CourseStat
from .CourseType import CourseType


class CourseStatType(DjangoObjectType):
    avg_rating = graphene.Decimal()

    class Meta:
        model = CourseStat
        interfaces = (relay.Node,)
        fields = (
            'id', 'count_comments', 'count_five_rating', 'count_four_rating',
            'count_three_rating', 'count_two_rating', 'count_one_rating',
        )

    def resolve_avg_rating(self, info):
        return self.course.avg_rating


class CourseStatQuery(graphene.ObjectType):
    statistic = graphene.Field(CourseStatType,
                               course_id=graphene.ID(required=True))

    def resolve_statistic(root, info, **kwargs):
        type_, course_id = from_global_id(kwargs.get('course_id'))

        if type_ != CourseType.__name__:
            raise GraphQLError('courseId: not valid value.')

        try:
            return CourseStat.objects.get(course_id=course_id)
        except ObjectDoesNotExist:
            raise GraphQLError('CourseId is Not Found.')
