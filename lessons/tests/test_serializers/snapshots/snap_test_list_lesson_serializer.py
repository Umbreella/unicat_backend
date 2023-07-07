# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ListLessonSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListLessonSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(help_text='Lesson name.', max_length=255, required=False)
    lesson_type = ChoiceField(choices=[(1, 'Тема'), (2, 'Теория'), (3, 'Тест')], help_text='Type of lesson.', validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    serial_number = SerializerMethodField()
    parent = PrimaryKeyRelatedField(allow_null=True, help_text='Parent lesson in relation to the current.', queryset=Lesson.objects.all(), required=False)'''
