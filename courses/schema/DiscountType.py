from graphene_django import DjangoObjectType

from ..models.Discount import Discount


class DiscountType(DjangoObjectType):
    class Meta:
        model = Discount
        fields = ('percent', 'end_date',)
