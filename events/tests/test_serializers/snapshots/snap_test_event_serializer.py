# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['EventSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''EventSerializer():
    id = IntegerField(label='ID', read_only=True)
    preview = Base64ImageField(required=False)
    title = CharField(max_length=255, required=False)
    short_description = CharField(max_length=255, required=False)
    description = CharField(style={'base_template': 'textarea.html'})
    date = DateField()
    start_time = TimeField()
    end_time = TimeField()
    place = CharField(max_length=255, required=False)
    created_at = DateTimeField(required=False)'''
