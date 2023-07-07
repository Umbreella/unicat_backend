# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ResourceSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ResourceSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(help_text='The file name given by the user.', max_length=255)
    file = Base64ImageField()
    loaded_at = DateTimeField(help_text='File upload time.', required=False)'''
