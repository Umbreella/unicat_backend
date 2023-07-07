from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.Teacher import Teacher
from ..serializers.ListTeacherSerializer import ListTeacherSerializer
from ..serializers.TeacherSerializer import TeacherSerializer


class TeacherView(ModelViewSet):
    queryset = Teacher.objects.select_related('user').all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = TeacherSerializer
    filter_backends = (OrderingFilter,)
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ListTeacherSerializer
        return super().list(self, request, *args, **kwargs)
