from django.core.exceptions import ObjectDoesNotExist
from graphql_relay import from_global_id
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from courses.models.Course import Course
from courses.schema.CourseType import CourseType


class PaymentCourseSerializer(serializers.Serializer):
    course_id = serializers.CharField(min_length=16, max_length=40)

    def validate(self, attrs):
        type_, course_id = from_global_id(attrs.get('course_id'))

        if type_ != CourseType.__name__:
            detail = {
                'course_id': [
                    'Not valid value.',
                ],
            }
            raise ValidationError(detail)

        try:
            self.course = Course.objects.get(pk=course_id)
        except ObjectDoesNotExist:
            detail = {
                'course_id': [
                    'This course is not found.',
                ],
            }
            raise ValidationError(detail)

        if not self.course.is_published:
            detail = {
                'course_id': [
                    'This course in archive.',
                ],
            }
            raise ValidationError(detail)

        return {
            'course_id': self.course.id,
        }
