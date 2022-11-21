from rest_framework.generics import CreateAPIView


class LogoutUserView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass
        # user = request.user
        #
        # return Response('', status=status.HTTP_200_OK)
