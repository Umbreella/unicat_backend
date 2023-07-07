from django.core.exceptions import ObjectDoesNotExist
from graphql_relay import from_global_id
from rest_framework.permissions import BasePermission

from courses.models.UserCourse import UserCourse

from ..models.Lesson import Lesson


class HasLessonPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        type_, lesson_id = from_global_id(view.kwargs.get('lesson_id'))

        if type_ != 'LessonType':
            return False

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except ObjectDoesNotExist:
            return False

        has_access = UserCourse.objects.filter(**{
            'user': user,
            'course': lesson.course,
        }).exists()

        view.kwargs.update({
            'lesson_id': lesson.id,
        })

        return has_access
