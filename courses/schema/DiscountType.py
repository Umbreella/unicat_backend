import graphene
from graphene_django import DjangoObjectType

from ..models.Discount import Discount


class DiscountType(DjangoObjectType):
    end_date = graphene.Date()

    class Meta:
        model = Discount
        fields = (
            'percent', 'end_date',
        )
