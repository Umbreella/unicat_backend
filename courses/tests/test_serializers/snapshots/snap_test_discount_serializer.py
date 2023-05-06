# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['DiscountSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''DiscountSerializer():
    id = IntegerField(label='ID', read_only=True)
    course = PrimaryKeyRelatedField(queryset=Course.objects.all())
    percent = IntegerField(max_value=100, min_value=1)
    start_date = DateTimeField()
    end_date = DateTimeField()'''
