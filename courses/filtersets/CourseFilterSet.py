from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter
from graphql import GraphQLError
from graphql_relay import from_global_id

from ..schema.CategoryType import CategoryType


class CourseFilterSet(FilterSet):
    order_by = OrderingFilter(
        fields=('created_at', 'price', 'avg_rating',)
    )
    search = CharFilter(field_name='title', lookup_expr='icontains')
    category_id = CharFilter(method='_filter_by_category')
    min_rating = NumberFilter(field_name='avg_rating', lookup_expr='gte')
    max_rating = NumberFilter(field_name='avg_rating', lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    def _filter_by_category(self, queryset, name, value):
        type_, category_id = from_global_id(value)

        if type_ != CategoryType.__name__:
            raise GraphQLError('category_id: not valid value.')

        lookup = {
            'category_id': category_id,
        }

        return queryset.filter(**lookup)
