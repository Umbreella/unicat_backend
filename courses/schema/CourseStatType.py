import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from unicat.graphql.functions import get_id_from_value

from ..models.CourseStat import CourseStat
from .CourseType import CourseType


class CourseStatType(DjangoObjectType):
    class Meta:
        model = CourseStat
        interfaces = (relay.Node,)
        fields = (
            'id', 'avg_rating', 'count_comments', 'count_five_rating',
            'count_four_rating', 'count_three_rating', 'count_two_rating',
            'count_one_rating',
        )


class CourseStatQuery(graphene.ObjectType):
    statistic = graphene.Field(CourseStatType,
                               course_id=graphene.ID(required=True))

    def resolve_statistic(root, info, **kwargs):
        course_id_b64 = kwargs['course_id']

        try:
            course_id = get_id_from_value(CourseType, course_id_b64)
        except Exception as ex:
            raise GraphQLError(ex)

        return CourseStat.objects.filter(course_id=course_id).first()
