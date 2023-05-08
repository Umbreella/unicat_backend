# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['AnswerValueSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''AnswerValueSerializer():
    id = IntegerField(label='ID', read_only=True)
    question = PrimaryKeyRelatedField(queryset=<QuerySet []>, required=False)
    value = CharField(max_length=128)
    is_true = BooleanField(required=False)'''
