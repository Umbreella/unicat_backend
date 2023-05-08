# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['LessonSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''LessonSerializer():
    id = IntegerField(label='ID', read_only=True)
    course = PrimaryKeyRelatedField(queryset=Course.objects.all())
    title = CharField(max_length=255, required=False)
    lesson_type = ChoiceField(choices=[(1, 'Тема'), (2, 'Теория'), (3, 'Тест')], validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    description = CharField(max_length=255, required=False)
    body = CharField(required=False, source='lesson_body.body')
    parent = PrimaryKeyRelatedField(allow_null=True, queryset=Lesson.objects.all(), required=False)
    questions = QuestionSerializer(many=True, required=False):
        id = IntegerField(label='ID', read_only=True)
        body = CharField(max_length=512)
        question_type = ChoiceField(choices=[(1, 'Один вариант'), (2, 'Несколько вариантов'), (3, 'Свободный ответ')], validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
        lesson = PrimaryKeyRelatedField(queryset=<QuerySet [<Lesson: Lesson object (1)>]>, required=False)
        answers = AnswerValueSerializer(many=True, write_only=True):
            id = IntegerField(label='ID', read_only=True)
            question = PrimaryKeyRelatedField(queryset=<QuerySet []>, required=False)
            value = CharField(max_length=128)
            is_true = BooleanField(required=False)'''
