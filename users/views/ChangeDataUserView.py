from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.ChangeDataUserSerializer import ChangeDataUserSerializer


class ChangeDataUserView(UpdateAPIView):
    serializer_class = ChangeDataUserSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        data = request.data
        current_user = request.user

        serializer = self.serializer_class(current_user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        data = request.data
        current_user = request.user

        serializer = self.serializer_class(current_user, data=data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
