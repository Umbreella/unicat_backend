from django_filters import CharFilter

from unicat.graphql.functions import get_id_from_value

from ..models.CommentedType import CommentedType
from .CommentFilterSet import CommentFilterSet


class CommentCourseFilterSet(CommentFilterSet):
    course_id = CharFilter(method='course_comments')

    def course_comments(self, queryset, name, value):
        course_id = get_id_from_value(value)

        lookup = {
            'commented_type': CommentedType.COURSE.value,
            'commented_id': course_id
        }

        return queryset.filter(**lookup)
