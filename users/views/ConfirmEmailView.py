from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.ConfirmEmailSerializer import ConfirmEmailSerializer


class ConfirmEmailView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmEmailSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'data': 'Email has been confirmed.', },
                        status=status.HTTP_200_OK)
