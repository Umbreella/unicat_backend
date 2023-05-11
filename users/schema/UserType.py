import graphene
from graphene_django import DjangoObjectType

from ..models import User


class UserType(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = User
        fields = (
            'name', 'photo',
        )

    def resolve_photo(self, info):
        if self.photo:
            return info.context.build_absolute_uri(self.photo.url)

        return None

    def resolve_name(self, info):
        return str(self)
