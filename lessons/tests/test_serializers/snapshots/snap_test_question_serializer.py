# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['QuestionSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''QuestionSerializer():
    id = IntegerField(label='ID', read_only=True)
    body = CharField(max_length=512)
    question_type = ChoiceField(choices=[(1, 'Один вариант'), (2, 'Несколько вариантов'), (3, 'Свободный ответ')], validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    lesson = PrimaryKeyRelatedField(queryset=<QuerySet [<Lesson: Lesson object (1)>, <Lesson: Lesson object (2)>]>, required=False)
    answers = AnswerValueSerializer(many=True, write_only=True):
        id = IntegerField(label='ID', read_only=True)
        question = PrimaryKeyRelatedField(queryset=<QuerySet [<Question: Question object (1)>]>, required=False)
        value = CharField(max_length=128)
        is_true = BooleanField(required=False)'''
