from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer


class LogoutUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenBlacklistSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        refresh_token_path = '/api/user/token'

        response = Response()
        response.data = {'data': 'Token destroyed.', }
        response.status_code = status.HTTP_200_OK

        response.delete_cookie(**{
            'key': 'refresh',
            'path': refresh_token_path,
            'domain': None,
            'samesite': 'strict',
        })

        return response
