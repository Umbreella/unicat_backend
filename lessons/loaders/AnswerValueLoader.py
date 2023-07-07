from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models.AnswerValue import AnswerValue
from ..models.QuestionTypeChoices import QuestionTypeChoices


class AnswerValueLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(answer_value_loader)


def answer_value_loader(keys: List[int]) -> List[List[AnswerValue]]:
    answers_queryset = AnswerValue.objects.select_related(
        'question'
    ).filter(**{
        'question_id__in': keys,
    }).order_by('?')

    answers_map = {}

    for answer in answers_queryset:
        answers = answers_map.get(answer.question_id)

        if answer.question.question_type == QuestionTypeChoices.FREE.value:
            answers = []
        elif not answers:
            answers = [answer, ]
        else:
            answers.append(answer)

        answers_map[answer.question_id] = answers

    return [answers_map.get(key, []) for key in keys]
