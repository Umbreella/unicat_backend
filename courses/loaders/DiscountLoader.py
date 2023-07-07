from typing import List

from django.utils import timezone
from graphql_sync_dataloaders import SyncDataLoader

from ..models.Discount import Discount


class DiscountLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(discount_loader)


def discount_loader(keys: List[int]) -> List[Discount]:
    discounts = Discount.objects.filter(**{
        'course_id__in': keys,
        'start_date__lte': timezone.now(),
        'end_date__gte': timezone.now(),
    })
    discount_map = {discount.course_id: discount for discount in discounts}

    return [discount_map.get(key, None) for key in keys]
