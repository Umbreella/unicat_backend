# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ListLessonSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListLessonSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=255, required=False)
    lesson_type = ChoiceField(choices=[(1, 'Тема'), (2, 'Теория'), (3, 'Тест')], validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    serial_number = IntegerField(max_value=32767, min_value=0, required=False)
    parent = PrimaryKeyRelatedField(allow_null=True, queryset=Lesson.objects.all(), required=False)'''
