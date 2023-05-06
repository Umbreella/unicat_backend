# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['FeedbackSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''FeedbackSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(max_length=255)
    email = EmailField(max_length=128)
    body = CharField(style={'base_template': 'textarea.html'})
    created_at = DateTimeField(required=False)
    is_closed = BooleanField(required=False)'''
