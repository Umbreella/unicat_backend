# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['ListUserSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''ListUserSerializer():
    id = IntegerField(label='ID', read_only=True)
    email = EmailField(help_text='User`s unique email address.', max_length=128, validators=[<UniqueValidator(queryset=User.objects.all())>])
    first_name = CharField(allow_blank=True, help_text='Username.', max_length=128, required=False)
    last_name = CharField(allow_blank=True, help_text='User`s last name.', max_length=128, required=False)
    is_staff = BooleanField(help_text='Does the user have access to the administration panel.', required=False)'''
