# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ListEventSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListEventSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=255, required=False)
    date = DateField()
    start_time = TimeField()
    end_time = TimeField()
    place = CharField(max_length=255, required=False)'''
