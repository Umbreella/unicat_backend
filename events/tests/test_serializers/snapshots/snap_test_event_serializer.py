# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['EventSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''EventSerializer():
    id = IntegerField(label='ID', read_only=True)
    preview = Base64ImageField(required=False)
    title = CharField(help_text='Event name.', max_length=255, required=False)
    short_description = CharField(help_text='A brief description of the event displayed on the icon.', max_length=255, required=False)
    description = CharField(help_text='Full description of the event.', style={'base_template': 'textarea.html'})
    date = DateField(help_text='Event date.')
    start_time = TimeField(help_text='Event start time.')
    end_time = TimeField(help_text='Event end time.')
    place = CharField(help_text='Venue of the event.', max_length=255, required=False)
    created_at = DateTimeField(help_text='Event creation time.', required=False)'''
