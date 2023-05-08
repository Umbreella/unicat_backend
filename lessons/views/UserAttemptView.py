from django.db.models import F, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.UserAttempt import UserAttempt
from ..models.UserLesson import UserLesson
from ..permissions.HasLessonPermission import HasLessonPermission
from ..serializers.UserAttemptSerializer import UserAttemptSerializer


class UserAttemptView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, HasLessonPermission,)
    serializer_class = UserAttemptSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        lesson_id = kwargs.get('lesson_id')

        user_lesson, is_created = UserLesson.objects.get_or_create(**{
            'lesson_id': lesson_id,
            'user': user,
        })

        filter_by_time_end = Q()
        filter_by_time_end_gt = Q(time_end__gt=timezone.now())
        filter_by_time_end_is_null = Q(time_end__isnull=True)
        filter_by_time_end.add(filter_by_time_end_gt, Q.OR)
        filter_by_time_end.add(filter_by_time_end_is_null, Q.OR)

        filter_result = Q()
        filter_by_user_lesson = Q(user_lesson=user_lesson)
        filter_result.add(filter_by_user_lesson, Q.AND)
        filter_result.add(filter_by_time_end, Q.AND)

        order_result = F('time_end').desc(nulls_last=True)

        active_attempt = UserAttempt.objects.using(
            'master'
        ).filter(
            filter_by_time_end
        ).order_by(
            order_result
        ).first()

        if active_attempt is None:
            detail = {
                'data': 'No active attempt.',
            }
            return Response(detail, status=status.HTTP_200_OK)

        serializer = self.serializer_class(active_attempt)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = {
            'lesson_id': kwargs.get('lesson_id'),
        }

        serializer = self.serializer_class(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
