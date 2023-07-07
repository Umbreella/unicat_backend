# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['UserSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''UserSerializer():
    id = IntegerField(label='ID', read_only=True)
    email = EmailField(help_text='User`s unique email address.', max_length=128, validators=[<UniqueValidator(queryset=User.objects.all())>])
    password = CharField(help_text='User password.', max_length=128)
    first_name = CharField(allow_blank=True, help_text='Username.', max_length=128, required=False)
    last_name = CharField(allow_blank=True, help_text='User`s last name.', max_length=128, required=False)
    photo = Base64ImageField(required=False)
    is_staff = BooleanField(help_text='Does the user have access to the administration panel.', required=False)
    groups = PrimaryKeyRelatedField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', many=True, queryset=Group.objects.all(), required=False)
    user_permissions = PrimaryKeyRelatedField(help_text='Specific permissions for this user.', many=True, queryset=Permission.objects.all(), required=False)'''
