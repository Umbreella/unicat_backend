from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template.loader import get_template
from django_weasyprint import WeasyTemplateResponseMixin
from graphql_relay import from_global_id
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from weasyprint import CSS, HTML

from ..models.UserCourse import UserCourse
from ..schema.CourseType import CourseType


class UserCertificateView(ListAPIView, WeasyTemplateResponseMixin):
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

        html_template = get_template('Certificate.html')
        context = {
            'title': 'Custom Title',
            'user': str(user_data),
            'course': course_data,
            'teacher': teacher_data,
            'completed_at': user_course.completed_at.strftime('%d-%m-%Y'),
            'progress': round((count_completed_lessons / count_lessons) * 100),
        }
        rendered_html = html_template.render(context)

        html_doc = HTML(string=rendered_html,
                        base_url=request.build_absolute_uri())
        styles = CSS(string="""
        @page {
            size: landscape;
            margin: 0.5cm;
            }
        """)
        pdf = html_doc.write_pdf(stylesheets=[styles])

        return HttpResponse(pdf, content_type='application/pdf')
