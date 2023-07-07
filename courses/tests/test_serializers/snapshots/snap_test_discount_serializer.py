# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['DiscountSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''DiscountSerializer():
    id = IntegerField(label='ID', read_only=True)
    course = PrimaryKeyRelatedField(help_text='The course for which the discount was created.', queryset=Course.objects.all())
    percent = IntegerField(help_text='Discount percentage, from 0 to 100.', max_value=100, min_value=1)
    start_date = DateTimeField(help_text='Discount start date.')
    end_date = DateTimeField(help_text='Discount end date.')'''
