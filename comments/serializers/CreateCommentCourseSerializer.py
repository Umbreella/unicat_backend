from django.core.exceptions import ValidationError as DjValidationError
from graphql_relay import from_global_id
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from courses.schema.CourseType import CourseType

from ..models.Comment import Comment
from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CreateCommentSerializer import CreateCommentSerializer


class CreateCommentCourseSerializer(CreateCommentSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    def validate(self, attrs):
        type_, commented_id = from_global_id(attrs.get('commented_id'))

        if type_ != CourseType.__name__:
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
            'commented_type': CommentedTypeChoices.COURSE.value,
        })

        try:
            comment = Comment.objects.create(**data)
        except DjValidationError as ex:
            raise ValidationError(ex.message_dict)

        return comment
