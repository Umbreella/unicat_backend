import copy

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.UserAnswerSerializer import UserAnswerSerializer


class UserAnswerView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAnswerSerializer

    def post(self, request, *args, **kwargs):
        data = copy.copy(request.data)
        user = request.user

        attempt_id = kwargs.get('attempt_id')
        data.update({
            'attempt_id': attempt_id,
        })

        serializer = self.serializer_class(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'data': 'Answer accepted.', },
                        status=status.HTTP_201_CREATED)
