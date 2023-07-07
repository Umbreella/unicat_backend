# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['FeedbackSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''FeedbackSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(help_text='Full name of the user who wrote.', max_length=255)
    email = EmailField(help_text='Email of the user who wrote.', max_length=128)
    body = CharField(help_text='Message content.', style={'base_template': 'textarea.html'})
    created_at = DateTimeField(help_text='Date of writing the message.', required=False)
    is_closed = BooleanField(help_text='Has the message been processed.', required=False)'''
