import graphene
from django.core.cache import cache
from graphene import String, relay
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from ..models.Question import Question
from ..models.QuestionTypeChoices import QuestionTypeChoices
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
        question_type = self.question_type

        if question_type == QuestionTypeChoices.FREE.value:
            return []

        return self.answers.order_by('?')


class QuestionConnection(relay.Connection):
    class Meta:
        node = QuestionType


class QuestionQuery(graphene.ObjectType):
    questions = graphene.List(QuestionType, attempt_id=String(required=True))

    @login_required
    def resolve_questions(root, info, *args, **kwargs):
        global_attempt_id = kwargs.get('attempt_id')
        attempt = relay.Node.get_node_from_global_id(info, global_attempt_id)

        if not isinstance(attempt, UserAttempt):
            raise GraphQLError('Not valid attemptId')

        if attempt.user_lesson.user != info.context.user:
            raise GraphQLError('You don`t have access on this attempt.')

        cache_key = f'{global_attempt_id}_answered_questions'
        answered_questions_ids = cache.get(cache_key, [])

        lesson_id = attempt.user_lesson.lesson_id
        filter_fields = {
            'lesson_id': lesson_id,
        }
        exclude_fields = {
            'id__in': answered_questions_ids,
        }

        data = Question.objects.filter(
            **filter_fields
        ).exclude(
            **exclude_fields
        ).order_by('?')

        return data
