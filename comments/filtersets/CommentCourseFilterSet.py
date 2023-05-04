from django_filters import CharFilter
from graphql import GraphQLError

from courses.schema.CourseType import CourseType
from unicat.graphql.functions import get_id_from_value

from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CommentFilterSet import CommentFilterSet


class CommentCourseFilterSet(CommentFilterSet):
    course_id = CharFilter(method='course_comments')

    def course_comments(self, queryset, name, value):
        try:
            course_id = get_id_from_value(CourseType, value)
        except Exception as ex:
            detail = f'course_id: {ex}'
            raise GraphQLError(detail)

        lookup = {
            'commented_type': CommentedTypeChoices.COURSE.value,
            'commented_id': course_id,
        }

        return queryset.filter(**lookup)
