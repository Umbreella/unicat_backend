from rest_framework.serializers import CharField, ModelSerializer

from ..models.Payment import Payment


class PaymentSerializer(ModelSerializer):
    user = CharField()
    course = CharField()

    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'course', 'amount', 'created_at',
        )
