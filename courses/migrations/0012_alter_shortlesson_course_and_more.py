# Generated by Django 4.1.2 on 2022-12-07 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_alter_shortlesson_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortlesson',
            name='course',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course'),
        ),
        migrations.AlterField(
            model_name='shortlesson',
            name='parent_lesson',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.shortlesson'),
        ),
        migrations.AlterField(
            model_name='shortlesson',
            name='serial_number',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
    ]