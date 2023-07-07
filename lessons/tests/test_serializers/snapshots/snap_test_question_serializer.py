# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['QuestionSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''QuestionSerializer():
    id = IntegerField(label='ID', read_only=True)
    body = CharField(help_text='Question body.', max_length=512)
    question_type = ChoiceField(choices=[(1, 'Один вариант'), (2, 'Несколько вариантов'), (3, 'Свободный ответ')], help_text='Question type by the number of correct answers.', validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    lesson = PrimaryKeyRelatedField(help_text='The lesson to which this question relates.', queryset=Lesson.objects.all())'''
