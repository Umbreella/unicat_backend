from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from courses.models.Course import Course
from courses.schema.CourseType import CourseType
from unicat.graphql.functions import get_id_from_value


class PaymentCourseSerializer(serializers.Serializer):
    course_id = serializers.CharField(min_length=16, max_length=40)

    def validate(self, attrs):
        course_id_b64 = attrs.get('course_id')

        try:
            course_id = get_id_from_value(CourseType, course_id_b64)
        except Exception as ex:
            detail = {
                'course_id': [
                    ex,
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

        return {
            'course_id': course_id,
        }
