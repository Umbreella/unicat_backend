from rest_framework.serializers import ModelSerializer

from ..models.Discount import Discount


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = (
            'id', 'course', 'percent', 'start_date', 'end_date',
        )
