# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['CourseSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''CourseSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=128, required=False)
    price = DecimalField(decimal_places=2, max_digits=7)
    count_lectures = IntegerField(max_value=32767, min_value=0, required=False)
    count_independents = IntegerField(max_value=32767, min_value=0, required=False)
    learning_format = ChoiceField(choices=[(1, 'Дистанционно'), (2, 'Очно'), (3, 'Очно-заочно')], validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    category = PrimaryKeyRelatedField(allow_null=True, queryset=Category.objects.all(), required=False)
    teacher = PrimaryKeyRelatedField(allow_null=True, queryset=Teacher.objects.all(), required=False)
    preview = Base64ImageField(required=False)
    short_description = CharField(max_length=255, required=False)
    body = CharField(source='course_body.body')'''
