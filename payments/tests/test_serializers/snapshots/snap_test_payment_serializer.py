# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['PaymentSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''PaymentSerializer():
    id = CharField(help_text='Payment intent ID from StripeAPI.', max_length=27, validators=[<UniqueValidator(queryset=Payment.objects.all())>])
    user = CharField()
    course = CharField()
    amount = DecimalField(decimal_places=2, help_text='Amount of payment.', max_digits=9)
    created_at = DateTimeField(help_text='Payment creation time.', required=False)'''
