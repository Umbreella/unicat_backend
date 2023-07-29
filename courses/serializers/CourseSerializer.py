from django.core.exceptions import ValidationError as DjValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer

from ..models.Course import Course
from ..models.CourseBody import CourseBody


class CourseSerializer(ModelSerializer):
    body = CharField(source='course_body.body')
    preview = Base64ImageField(required=False)

    class Meta:
        model = Course
        fields = (
            'id', 'title', 'price', 'count_lectures', 'count_independents',
            'learning_format', 'category', 'teacher', 'preview',
            'short_description', 'body', 'is_published',
        )

    def create(self, validated_data):
        body = validated_data.pop('course_body')

        try:
            course = Course.objects.create(**validated_data)
        except DjValidationError as ex:
            raise ValidationError(ex.message_dict)

        CourseBody.objects.create(**{
            **body,
            'course': course,
        })

        return course

    def update(self, instance, validated_data):
        if 'course_body' in validated_data:
            body = validated_data.pop('course_body')['body']
            course_body = instance.course_body
            course_body.body = body
            course_body.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
