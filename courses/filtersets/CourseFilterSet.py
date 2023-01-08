from django_filters import CharFilter, FilterSet, OrderingFilter

from unicat.graphql.functions import get_id_from_value


class CourseFilterSet(FilterSet):
    order_by = OrderingFilter(
        fields=('created_at', 'price', )
    )

    search = CharFilter(method='search_by_title')
    category = CharFilter(method='filter_by_category')

    def search_by_title(self, queryset, name, value):
        lookup = {
            'title__icontains': value,
        }

        return queryset.filter(**lookup)

    def filter_by_category(self, queryset, name, value):
        category_id = get_id_from_value(value)

        lookup = {
            'category_id': category_id,
        }

        return queryset.filter(**lookup)
