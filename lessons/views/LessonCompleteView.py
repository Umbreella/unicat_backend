from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..permissions.HasLessonPermission import HasLessonPermission
from ..serializers.LessonCompleteSerializer import LessonCompleteSerializer


class LessonCompleteView(CreateAPIView):
    permission_classes = (IsAuthenticated, HasLessonPermission,)
    serializer_class = LessonCompleteSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = {
            'lesson_id': kwargs.get('lesson_id'),
        }

        serializer = self.serializer_class(data=data, context={'user': user, })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'data': 'Lesson is complete.', },
                        status=status.HTTP_201_CREATED)
