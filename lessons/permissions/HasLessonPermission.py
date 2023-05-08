from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from courses.models.UserCourse import UserCourse
from unicat.graphql.functions import get_id_from_value

from ..models.Lesson import Lesson
from ..schema.LessonType import LessonType


class HasLessonPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        lesson_id = view.kwargs.get('lesson_id')

        try:
            lesson_id = get_id_from_value(LessonType, lesson_id)
        except Exception:
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
