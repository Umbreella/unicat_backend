from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
from graphql_relay import to_global_id
from rest_framework.exceptions import ValidationError

from ..models.UserAttempt import UserAttempt
from .UserAttemptSerializer import UserAttemptSerializer


class UserAttemptRefreshSerializer(UserAttemptSerializer):
    def save(self, **kwargs):
        lesson_id = self.validated_data.get('lesson_id')

        filter_by_time_end = Q()
        filter_by_time_end_gt = Q(time_end__gt=timezone.now())
        filter_by_time_end_is_null = Q(time_end__isnull=True)
        filter_by_time_end.add(filter_by_time_end_gt, Q.OR)
        filter_by_time_end.add(filter_by_time_end_is_null, Q.OR)

        filter_by_lesson = Q(user_lesson__lesson_id=lesson_id)

        filter_queryset = Q()
        filter_queryset.add(filter_by_time_end, Q.AND)
        filter_queryset.add(filter_by_lesson, Q.AND)

        try:
            user_attempt = UserAttempt.objects.get(filter_queryset)
        except ObjectDoesNotExist:
            detail = {
                'lesson_id': [
                    'Active attempt is not found.',
                ],
            }
            raise ValidationError(detail)

        user_attempt.time_end = timezone.now()
        user_attempt.save()

        attempt_global_id = to_global_id('UserAttemptType', user_attempt.id)
        cache_key = f'{attempt_global_id}_answered_questions'
        cache.delete(cache_key)

        self.instance = self.create(self.validated_data)

        return self.instance
