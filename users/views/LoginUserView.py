from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.LoginUserSerializer import LoginUserSerializer


class LoginUserView(CreateAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        serialized_data = serializer.data
        refresh_token = serialized_data['refresh']
        refresh_token_path = '/api/user/token'

        response = Response()
        response.data = serialized_data
        response.status_code = status.HTTP_200_OK

        response.set_cookie(
            key='refresh',
            value=refresh_token,
            path=refresh_token_path,
            domain=None,
            secure=True,
            httponly=True,
            samesite='strict'
        )

        return response
