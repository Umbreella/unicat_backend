from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..filtersets.LessonParentFilter import LessonParentFilter
from ..models.Lesson import Lesson
from ..serializers.LessonSerializer import LessonSerializer
from ..serializers.ListLessonSerializer import ListLessonSerializer


class LessonView(ModelViewSet):
    queryset = Lesson.objects.prefetch_related('lesson_body').all()
    permission_classes = (IsAdminUser,)
    serializer_class = LessonSerializer
    filter_backends = (LessonParentFilter, DjangoFilterBackend, SearchFilter,
                       OrderingFilter,)
    filterset_fields = ('course_id', 'parent',)
    search_fields = ('title',)
    ordering_fields = '__all__'
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        self.queryset = Lesson.objects.all()
        self.serializer_class = ListLessonSerializer
        return super().list(self, request, *args, **kwargs)
