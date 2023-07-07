from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models.Category import Category


class CategoryLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(category_loader)


def category_loader(keys: List[int]) -> List[Category]:
    categories = Category.objects.filter(**{
        'id__in': keys,
    })
    category_map = {category.id: category for category in categories}

    return [category_map.get(key, None) for key in keys]
