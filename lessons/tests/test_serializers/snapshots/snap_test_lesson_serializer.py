# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['LessonSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''LessonSerializer():
    id = IntegerField(label='ID', read_only=True)
    course = PrimaryKeyRelatedField(help_text='The course that the lesson belongs to.', queryset=Course.objects.all())
    serial_number = IntegerField(help_text='Sequence number of the lesson.', max_value=32767, min_value=0, required=False)
    title = CharField(help_text='Lesson name.', max_length=255, required=False)
    lesson_type = ChoiceField(choices=[(1, 'Тема'), (2, 'Теория'), (3, 'Тест')], help_text='Type of lesson.', validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    description = CharField(help_text='A brief description of the lesson, which is displayed in the course content tab.', max_length=255, required=False)
    body = CharField(required=False, source='lesson_body.body')
    parent = PrimaryKeyRelatedField(allow_null=True, help_text='Parent lesson in relation to the current.', queryset=Lesson.objects.all(), required=False)'''
