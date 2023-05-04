from django.core.exceptions import ValidationError as DjValidationError
from rest_framework.exceptions import ValidationError

from events.schema.EventType import EventType
from unicat.graphql.functions import get_id_from_value

from ..models.Comment import Comment
from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CreateCommentSerializer import CreateCommentSerializer


class CreateCommentEventSerializer(CreateCommentSerializer):
    def validate(self, attrs):
        commented_id_b64 = attrs['commented_id']

        try:
            commented_id = get_id_from_value(EventType, commented_id_b64)
        except Exception as ex:
            detail = {
                'commented_id': ex,
            }
            raise ValidationError(detail)

        attrs.update({
            'commented_id': commented_id
        })

        return attrs

    def create(self, validated_data):
        data = validated_data
        data.update({
            'author': self.context.get('user'),
            'commented_type': CommentedTypeChoices.EVENT.value,
        })

        try:
            comment = Comment.objects.create(**data)
        except DjValidationError as ex:
            raise ValidationError(ex.message_dict)

        return comment
