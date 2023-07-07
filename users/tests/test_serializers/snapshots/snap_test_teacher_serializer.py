# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['TeacherSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''TeacherSerializer():
    id = IntegerField(label='ID', read_only=True)
    user = PrimaryKeyRelatedField(help_text='User for whom the teacher record is added.', queryset=User.objects.all(), validators=[<UniqueValidator(queryset=Teacher.objects.all())>])
    description = CharField(help_text='Some words about teacher.', max_length=255)
    facebook = CharField(allow_blank=True, help_text='Link to the user`s Facebook page.', max_length=255, required=False)
    twitter = CharField(allow_blank=True, help_text='Link to the user`s Twitter page.', max_length=255, required=False)
    google_plus = CharField(allow_blank=True, help_text='Link to the user`s GooglePlus page.', max_length=255, required=False)
    vk = CharField(allow_blank=True, help_text='Link to the user`s VK page.', max_length=255, required=False)'''
