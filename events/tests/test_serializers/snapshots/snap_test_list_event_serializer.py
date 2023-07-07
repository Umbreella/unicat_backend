# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ListEventSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListEventSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(help_text='Event name.', max_length=255, required=False)
    date = DateField(help_text='Event date.')
    start_time = TimeField(help_text='Event start time.')
    end_time = TimeField(help_text='Event end time.')
    place = CharField(help_text='Venue of the event.', max_length=255, required=False)'''
