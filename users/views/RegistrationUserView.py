from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.RegistrationUserSerializer import RegistrationUserSerializer


class RegistrationUserView(CreateAPIView):
    serializer_class = RegistrationUserSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
