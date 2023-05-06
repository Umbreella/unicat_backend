# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['CategorySerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''CategorySerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=128)'''
