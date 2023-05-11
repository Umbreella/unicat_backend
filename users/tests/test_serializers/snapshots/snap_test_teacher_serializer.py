# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['TeacherSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''TeacherSerializer():
    id = IntegerField(label='ID', read_only=True)
    user = PrimaryKeyRelatedField(queryset=User.objects.all(), validators=[<UniqueValidator(queryset=Teacher.objects.all())>])
    description = CharField(max_length=255)
    facebook = CharField(allow_blank=True, max_length=255, required=False)
    twitter = CharField(allow_blank=True, max_length=255, required=False)
    google_plus = CharField(allow_blank=True, max_length=255, required=False)
    vk = CharField(allow_blank=True, max_length=255, required=False)'''
