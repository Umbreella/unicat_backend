from django_filters import FilterSet, OrderingFilter


class CategoryFilterSet(FilterSet):
    order_by = OrderingFilter(
        fields=('title', )
    )
