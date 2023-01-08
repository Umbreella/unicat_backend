from django_filters import FilterSet, OrderingFilter


class CommentFilterSet(FilterSet):
    order_by = OrderingFilter(
        fields=('created_at', )
    )
