from django.core.exceptions import ValidationError as DjValidationError
from graphql_relay import from_global_id
from rest_framework.exceptions import ValidationError

from events.schema.EventType import EventType

from ..models.Comment import Comment
from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CreateCommentSerializer import CreateCommentSerializer


class CreateCommentEventSerializer(CreateCommentSerializer):
    def validate(self, attrs):
        type_, commented_id = from_global_id(attrs.get('commented_id'))

        if type_ != EventType.__name__:
            detail = {
                'commented_id': [
                    'Not valid value.',
                ],
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
