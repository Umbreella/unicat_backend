import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from ..filtersets.PaymentFilterSet import PaymentFilterSet
from ..models.Payment import Payment


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        interfaces = (relay.Node,)
        fields = (
            'id', 'course', 'amount', 'created_at',
        )


class PaymentQuery(graphene.ObjectType):
    my_payments = DjangoFilterConnectionField(PaymentType,
                                              filterset_class=PaymentFilterSet)

    @login_required
    def resolve_my_payments(root, info, **kwargs):
        user = info.context.user

        return Payment.objects.filter(**{
            'user': user,
            'is_success': True,
        })
