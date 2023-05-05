# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['NewSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''NewSerializer():
    id = IntegerField(label='ID', read_only=True)
    preview = Base64ImageField(required=False)
    title = CharField(max_length=255, required=False)
    short_description = CharField(max_length=255, required=False)
    description = CharField(style={'base_template': 'textarea.html'})
    author = PrimaryKeyRelatedField(allow_null=True, queryset=User.objects.all(), required=False)
    created_at = DateTimeField(required=False)'''
