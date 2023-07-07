# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['CourseSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''CourseSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(help_text='Course name.', max_length=128, required=False)
    price = DecimalField(decimal_places=2, help_text='Course price.', max_digits=7)
    count_lectures = IntegerField(help_text='Count lectures in course, calculated automatically.', max_value=32767, min_value=0, required=False)
    count_independents = IntegerField(help_text='Count independents in course, calculated automatically.', max_value=32767, min_value=0, required=False)
    learning_format = ChoiceField(choices=[(1, 'Дистанционно'), (2, 'Очно'), (3, 'Очно-заочно')], validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
    category = PrimaryKeyRelatedField(allow_null=True, help_text='Course category.', queryset=Category.objects.all(), required=False)
    teacher = PrimaryKeyRelatedField(allow_null=True, help_text='The teacher who leads the course.', queryset=Teacher.objects.all(), required=False)
    preview = Base64ImageField(required=False)
    short_description = CharField(help_text='A few words about the course, shown on the course icon.', max_length=255, required=False)
    body = CharField(source='course_body.body')'''
