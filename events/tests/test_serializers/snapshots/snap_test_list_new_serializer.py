# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ListNewSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListNewSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(help_text='News name.', max_length=255, required=False)
    created_at = DateTimeField(help_text='News creation time.', required=False)'''
