from graphene import relay
from graphql_relay import to_global_id


class LessonTypeNode(relay.Node):
    @classmethod
    def to_global_id(cls, type_, id):
        from ..schema.LessonType import LessonType

        return to_global_id(LessonType.__name__, id)
