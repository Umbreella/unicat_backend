from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from graphql_relay import from_global_id
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from ..models.UserCourse import UserCourse
from ..schema.CourseType import CourseType


class UserCertificateView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Serializer

    def get(self, request, *args, **kwargs):
        user = request.user
        type_, course_id = from_global_id(kwargs.get('course_id'))

        if type_ != CourseType.__name__:
            detail = {
                'course_id': [
                    'Not valid value.',
                ],
            }
            raise ValidationError(detail)

        try:
            user_course = UserCourse.objects.get(**{
                'user': user,
                'course_id': course_id,
                'completed_at__isnull': False,
            })
        except ObjectDoesNotExist:
            detail = {
                'course_id': [
                    'You do not have a course certificate.',
                ],
            }
            raise ValidationError(detail)

        user_data = str(user)
        course = user_course.course
        course_data = course.title
        count_lessons = sum([
            user_course.course.count_lectures,
            user_course.course.count_independents,
        ])
        count_completed_lessons = sum([
            user_course.count_lectures_completed,
            user_course.count_independents_completed,
        ])
        teacher_data = str(course.teacher)

        context = {
            'title': course.title,
            'user': str(user_data),
            'course': course_data,
            'teacher': teacher_data,
            'completed_at': user_course.completed_at.strftime('%d-%m-%Y'),
            'progress': round((count_completed_lessons / count_lessons) * 100),
        }

        return render(**{
            'request': request,
            'template_name': 'Certificate.html',
            'context': context,
        })
