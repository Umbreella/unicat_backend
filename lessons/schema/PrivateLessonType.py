import graphene
from graphql_jwt.decorators import login_required

from .PublicLessonType import PublicLessonType


class PrivateLessonType(PublicLessonType):
    is_completed = graphene.Boolean()

    class Meta:
        model = PublicLessonType._meta.model
        interfaces = PublicLessonType._meta.interfaces
        fields = (
            'id', 'serial_number', 'title', 'description', 'lesson_type',
            'is_completed',
        )

    @login_required
    def resolve_is_completed(self, info):
        return info.context.loaders.user_lesson_loader.load(
            (self.id, info.context.user.id,)
        )
