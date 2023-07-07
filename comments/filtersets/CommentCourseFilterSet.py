from django_filters import CharFilter
from graphql import GraphQLError
from graphql_relay import from_global_id

from courses.schema.CourseType import CourseType

from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CommentFilterSet import CommentFilterSet


class CommentCourseFilterSet(CommentFilterSet):
    course_id = CharFilter(method='course_comments')

    def course_comments(self, queryset, name, value):
        type_, course_id = from_global_id(value)

        if type_ != CourseType.__name__:
            raise GraphQLError('course_id: not valid value.')

        lookup = {
            'commented_type': CommentedTypeChoices.COURSE.value,
            'commented_id': course_id,
        }

        return queryset.filter(**lookup)
