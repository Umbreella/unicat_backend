from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.Course import Course
from ..serializers.CourseSerializer import CourseSerializer
from ..serializers.ListCourseSerializer import ListCourseSerializer


class CourseView(ModelViewSet):
    queryset = Course.objects.prefetch_related('course_body').all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = CourseSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title',)
    ordering_fields = '__all__'
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        self.queryset = Course.objects.all()
        self.serializer_class = ListCourseSerializer
        return super().list(self, request, *args, **kwargs)
