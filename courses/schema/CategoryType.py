import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import \
    DjangoFilterConnectionField as DjFilterConnectionField

from ..filtersets.CategoryFilterSet import CategoryFilterSet
from ..models.Category import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (relay.Node,)
        fields = ('id', 'title',)


class CategoryQuery(graphene.ObjectType):
    all_categories = DjFilterConnectionField(CategoryType,
                                             filterset_class=CategoryFilterSet)
