import graphene
from django_filters import FilterSet, OrderingFilter
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ..models.Category import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (relay.Node,)
        fields = '__all__'


class CategoryFilter(FilterSet):
    order_by = OrderingFilter(
        fields=('title',),
    )


class CategoryQuery(graphene.ObjectType):
    all_categories = DjangoFilterConnectionField(CategoryType,
                                                 filterset_class=CategoryFilter
                                                 )
