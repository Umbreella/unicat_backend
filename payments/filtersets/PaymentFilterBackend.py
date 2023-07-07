from rest_framework.filters import BaseFilterBackend


class PaymentFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        created_at = request.query_params.get('created_at')

        if created_at:
            queryset = queryset.filter(created_at__date=created_at)

        return queryset
