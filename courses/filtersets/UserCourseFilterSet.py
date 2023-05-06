from django_filters import BooleanFilter, CharFilter, FilterSet
from graphql import GraphQLError


class UserCourseFilterSet(FilterSet):
    order_by = CharFilter(method='_order_by_fields')
    search = CharFilter(field_name='title', lookup_expr='icontains')
    is_completed = BooleanFilter(field_name='user_courses__completed_at',
                                 lookup_expr='isnull', exclude=True)

    def _order_by_fields(self, queryset, name, value):
        field_values = {
            'created_at': 'user_courses__created_at',
            '-created_at': '-user_courses__created_at',
            'last_view': 'user_courses__last_view',
            '-last_view': '-user_courses__last_view',
        }

        if value not in field_values.keys():
            detail = 'Not valid choices for orderBy.'
            raise GraphQLError(detail)

        return queryset.order_by(field_values[value])
