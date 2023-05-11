# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['PermissionSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''PermissionSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(max_length=255)'''
