from django_filters import FilterSet, OrderingFilter


class PaymentFilterSet(FilterSet):
    order_by = OrderingFilter(
        fields=('created_at',)
    )
