from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter
from graphql import GraphQLError

from unicat.graphql.functions import get_id_from_value

from ..schema.CategoryType import CategoryType


class CourseFilterSet(FilterSet):
    order_by = OrderingFilter(
        fields=('created_at', 'price', 'statistic__avg_rating',)
    )
    search = CharFilter(field_name='title', lookup_expr='icontains')
    category_id = CharFilter(method='_filter_by_category')
    min_rating = NumberFilter(field_name='statistic__avg_rating',
                              lookup_expr='gte')
    max_rating = NumberFilter(field_name='statistic__avg_rating',
                              lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    def _filter_by_category(self, queryset, name, value):
        try:
            category_id = get_id_from_value(CategoryType, value)
        except Exception as ex:
            detail = f'category_id: {ex}'
            raise GraphQLError(detail)

        lookup = {
            'category_id': category_id,
        }

        return queryset.filter(**lookup)
