# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['CommentSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''CommentSerializer():
    id = IntegerField(label='ID', read_only=True)
    author = PrimaryKeyRelatedField(queryset=User.objects.all())
    body = CharField(style={'base_template': 'textarea.html'})
    created_at = DateTimeField(required=False)'''
