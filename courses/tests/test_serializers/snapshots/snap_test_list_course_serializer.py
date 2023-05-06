# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['CourseSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListCourseSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=128, required=False)
    price = DecimalField(decimal_places=2, max_digits=7)
    count_lectures = IntegerField(max_value=32767, min_value=0, required=False)
    count_independents = IntegerField(max_value=32767, min_value=0, required=False)'''
