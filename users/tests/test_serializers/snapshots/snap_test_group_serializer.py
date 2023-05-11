# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['GroupSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''GroupSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(max_length=150, validators=[<UniqueValidator(queryset=Group.objects.all())>])
    permissions = PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)'''
