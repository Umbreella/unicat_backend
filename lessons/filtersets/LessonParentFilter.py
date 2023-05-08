from rest_framework.filters import BaseFilterBackend


class LessonParentFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        parent_only = request.query_params.get('parent_only')

        if parent_only and parent_only == 1:
            queryset = queryset.filter(**{
                'parent__isnull': True,
            })

        return queryset
