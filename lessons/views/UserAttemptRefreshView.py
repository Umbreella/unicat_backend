import copy

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..permissions.HasLessonPermission import HasLessonPermission
from ..serializers.UserAttemptRefreshSerializer import \
    UserAttemptRefreshSerializer


class UserAttemptRefreshView(CreateAPIView):
    permission_classes = (IsAuthenticated, HasLessonPermission,)
    serializer_class = UserAttemptRefreshSerializer

    def post(self, request, *args, **kwargs):
        data = copy.copy(request.data)
        user = request.user

        data.update({
            'lesson_id': kwargs.get('lesson_id'),
        })

        serializer = self.serializer_class(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
