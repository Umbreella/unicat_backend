# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ListTeacherSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListTeacherSerializer():
    id = IntegerField(label='ID', read_only=True)
    user = CharField()
    description = CharField(help_text='Some words about teacher.', max_length=255)'''
