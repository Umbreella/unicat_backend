from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models import User


class UserLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(user_loader)


def user_loader(keys: List[int]) -> List[User]:
    users = User.objects.filter(**{
        'id__in': keys,
    })
    users_map = {user.id: user for user in users}

    return [users_map.get(key, None) for key in keys]
