# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['CommentSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''CommentSerializer():
    id = IntegerField(label='ID', read_only=True)
    author = PrimaryKeyRelatedField(help_text='The user who wrote the comment.', queryset=User.objects.all())
    body = CharField(help_text='The text of the comment itself.', style={'base_template': 'textarea.html'})
    created_at = DateTimeField(help_text='Date the comment was written.', required=False)'''
