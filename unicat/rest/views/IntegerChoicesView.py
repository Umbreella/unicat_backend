from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ..serializers.IntegerChoicesSerializer import IntegerChoicesSerializer


class IntegerChoiceView(RetrieveAPIView):
    queryset = QuerySet()
    permission_classes = (IsAdminUser,)
    serializer_class = IntegerChoicesSerializer
    integer_choices = None

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        choices = self.integer_choices.choices

        if pk:
            response_data = self.__get_format_or_404(choices, pk)
        else:
            data = []
            for (id, label) in choices:
                data += [
                    {
                        'id': id,
                        'label': label,
                    },
                ]

            response_data = {
                'count': len(data),
                'next': None,
                'previous': None,
                'results': data,
            }

        return Response(response_data, status=status.HTTP_200_OK)

    def __get_format_or_404(self, choices, pk):
        data = list(filter(lambda item: item[0] == pk, choices))

        if not data:
            raise NotFound()

        return {
            'id': data[0][0],
            'label': data[0][1],
        }
