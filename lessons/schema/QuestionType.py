import graphene
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from graphene import String, relay
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from ..models.Question import Question
from ..models.UserAttempt import UserAttempt
from .AnswerValueType import AnswerValueType


class QuestionType(DjangoObjectType):
    question_type = graphene.Int()
    answers = graphene.List(AnswerValueType)

    class Meta:
        model = Question
        interfaces = (relay.Node,)
        fields = (
            'id', 'body', 'question_type',
        )

    def resolve_answers(self, info):
        return info.context.loaders.answer_value_loader.load(self.id)


class QuestionQuery(graphene.ObjectType):
    questions = graphene.List(QuestionType, attempt_id=String(required=True))

    @login_required
    def resolve_questions(root, info, *args, **kwargs):
        global_attempt_id = kwargs.get('attempt_id')

        type_, attempt_id = from_global_id(global_attempt_id)

        if type_ != 'UserAttemptType':
            raise GraphQLError('attemptId: not valid value.')

        try:
            attempt = UserAttempt.objects.select_related(
                'user_lesson'
            ).get(pk=attempt_id)
        except ObjectDoesNotExist:
            raise GraphQLError('attemptId: not found value.')

        if attempt.user_lesson.user != info.context.user:
            raise GraphQLError('You don`t have access on this attempt.')

        cache_key = f'{global_attempt_id}_answered_questions'
        answered_questions_ids = cache.get(cache_key, [])

        data = Question.objects.filter(**{
            'lesson_id': attempt.user_lesson.lesson_id,
        }).exclude(**{
            'id__in': answered_questions_ids,
        }).order_by('?')

        return data
